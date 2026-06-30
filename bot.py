import asyncio
import json
import os
import time
import uuid
import subprocess
from datetime import datetime
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes,
)


def load_env():
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())

load_env()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
PROJECT_ROOT = Path(__file__).parent
RESULTS_DIR = PROJECT_ROOT / "results"
HISTORY_FILE = PROJECT_ROOT / "bot_history.json"
ALLURE_DIR = PROJECT_ROOT / "allure-results"
SCHEDULE_FILE = PROJECT_ROOT / "bot_schedule.json"

TEST_SUITES = {
    "api": {"path": "tests/api/", "desc": "API тесты"},
    "ui": {"path": "tests/ui/", "desc": "UI тесты (Chrome)"},
    "unit": {"path": "tests/unit/", "desc": "Unit тесты"},
    "load": {"path": "load/", "desc": "Нагрузочные (locust)"},
}

SUITE_GROUPS = {
    "all": {"suites": ["api", "unit"], "desc": "Все (API + Unit)"},
    "api+unit": {"suites": ["api", "unit"], "desc": "API + Unit"},
    "api+load": {"suites": ["api", "load"], "desc": "API + Load"},
}


# ======================== История ========================

def load_history() -> list:
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text("utf-8"))
    return []


def save_history(entry: dict):
    history = load_history()
    history.insert(0, entry)
    history = history[:50]
    HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), "utf-8")


def add_history(suite: str, passed: int, failed: int, errors: int,
                elapsed: float, user: str = "unknown"):
    entry = {
        "id": str(uuid.uuid4())[:8],
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "suite": suite,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "elapsed": round(elapsed, 1),
        "user": user,
        "status": "OK" if failed == 0 and errors == 0 else "FAIL",
    }
    save_history(entry)


# ======================== Расписание ========================

def load_schedule() -> dict:
    if SCHEDULE_FILE.exists():
        return json.loads(SCHEDULE_FILE.read_text("utf-8"))
    return {"jobs": []}


def save_schedule(data: dict):
    SCHEDULE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")


# ======================== Утилиты ========================

async def run_cmd(cmd: str, timeout: int = 600) -> tuple:
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=str(PROJECT_ROOT),
    )
    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout)
    out = stdout.decode(errors="replace").strip()
    err = stderr.decode(errors="replace").strip()
    return proc.returncode, f"{out}\n{err}".strip()


def make_progress_bar(pct: float, length: int = 10) -> str:
    filled = int(length * pct / 100)
    bar = "█" * filled + "░" * (length - filled)
    return f"[{bar}] {pct:.0f}%"


def parse_pytest_output(output: str) -> dict:
    passed = failed = errors = skipped = 0
    for line in output.split("\n"):
        low = line.lower()
        if "passed" in low:
            for p in low.split():
                if p.isdigit():
                    passed = int(p)
                    break
        if "failed" in low:
            for p in low.split():
                if p.isdigit():
                    failed = int(p)
                    break
        if "error" in low:
            for p in low.split():
                if p.isdigit():
                    errors = int(p)
                    break
        if "skip" in low:
            for p in low.split():
                if p.isdigit():
                    skipped = int(p)
                    break
    return {"passed": passed, "failed": failed, "errors": errors, "skipped": skipped}


def format_beautiful(code: int, output: str, suite_name: str, elapsed: float) -> str:
    stats = parse_pytest_output(output)
    total = stats["passed"] + stats["failed"] + stats["errors"] + stats["skipped"]

    if total == 0:
        return f"Результат: не удалось запустить тесты\n\n{output[-500:]}"

    pct = (stats["passed"] / total * 100) if total else 0

    if stats["failed"] == 0 and stats["errors"] == 0:
        status_line = "Все тесты прошли"
    else:
        status_line = "Есть падения"

    lines = [
        f"Результат: {suite_name}",
        "",
        status_line,
        "",
    ]

    if total > 0:
        bar = make_progress_bar(pct, 15)
        lines.append(f"Пройдено: {stats['passed']}/{total} ({pct:.0f}%)")
        lines.append(bar)

    if stats["failed"]:
        lines.append(f"Упало: {stats['failed']}")
    if stats["errors"]:
        lines.append(f"Ошибок: {stats['errors']}")
    if stats["skipped"]:
        lines.append(f"Пропущено: {stats['skipped']}")

    lines.append(f"\nВремя: {elapsed:.1f}с")

    if stats["failed"] or stats["errors"]:
        fail_lines = [l.strip() for l in output.split("\n") if "FAILED" in l or "ERROR" in l]
        if fail_lines:
            lines.append("\nПадения:")
            for l in fail_lines[:8]:
                short = l.split("::")[-1] if "::" in l else l
                lines.append(f"  - {short}")
            if len(fail_lines) > 8:
                lines.append(f"  ... и ещё {len(fail_lines) - 8}")

    return "\n".join(lines)


# ======================== Хендлеры ========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Запустить все", callback_data="run:all")],
        [
            InlineKeyboardButton("API", callback_data="run:api"),
            InlineKeyboardButton("Unit", callback_data="run:unit"),
        ],
        [
            InlineKeyboardButton("UI", callback_data="run:ui"),
            InlineKeyboardButton("Load", callback_data="run:load"),
        ],
        [
            InlineKeyboardButton("API + Unit", callback_data="run:api+unit"),
            InlineKeyboardButton("API + Load", callback_data="run:api+load"),
        ],
        [
            InlineKeyboardButton("История", callback_data="menu:history"),
            InlineKeyboardButton("Расписание", callback_data="menu:schedule"),
        ],
    ]
    await update.message.reply_text(
        "Тест-бот the-white-house-project\n\nВыбери что запустить:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Команды:\n\n"
        "/start — меню с кнопками\n"
        "/history — последние запуски\n"
        "/schedule — расписание автозапусков\n"
        "/suites — список сьютов\n"
        "/status — сколько тестов\n"
        "/allure — ссылка на отчёт\n\n"
        "/run <путь> — конкретный файл\n"
        "  /run tests/api/test_api_methods.py"
    )
    keyboard = [[InlineKeyboardButton("Меню", callback_data="menu:run")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def suites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = ["Тест-сьюты:\n"]
    for name, info in TEST_SUITES.items():
        full = PROJECT_ROOT / info["path"]
        if full.exists():
            count = len(list(full.glob("test_*.py")))
            lines.append(f"  {name:8s} {info['desc']}  ({count} файлов)")
        else:
            lines.append(f"  {name:8s} {info['desc']}  (нет)")

    keyboard = [[InlineKeyboardButton("Запустить", callback_data="menu:run")]]
    await update.message.reply_text("\n".join(lines), reply_markup=InlineKeyboardMarkup(keyboard))


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Считаю тесты...")
    code, output = await run_cmd("python -m pytest --collect-only -q 2>&1", timeout=30)
    lines = output.strip().split("\n")
    total = len([l for l in lines if "::" in l or l.strip().isdigit()])
    await update.message.reply_text(f"Найдено тестов: {total}")


async def history_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    history = load_history()
    if not history:
        await update.message.reply_text("История пуста. Запусти тесты!")
        return

    lines = ["Последние запуски:\n"]
    for entry in history[:10]:
        icon = "OK" if entry["status"] == "OK" else "FAIL"
        lines.append(
            f"{icon} {entry['suite']}  "
            f"{entry['passed']}/{entry['passed'] + entry['failed'] + entry['errors']}  "
            f"{entry['elapsed']}с  "
            f"{entry['time']}"
        )

    keyboard = [[InlineKeyboardButton("Запустить", callback_data="menu:run")]]
    await update.message.reply_text("\n".join(lines), reply_markup=InlineKeyboardMarkup(keyboard))


async def allure_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ALLURE_DIR.exists() or not list(ALLURE_DIR.glob("*.json")):
        await update.message.reply_text("Отчётов пока нет. Запусти тесты с Allure.")
        return

    count = len(list(ALLURE_DIR.glob("*.json")))
    await update.message.reply_text(
        f"Allure отчёт: {count} результатов\n\n"
        "Для просмотра:\n"
        "1. allure serve allure-results\n"
        "2. allure open allure-report\n\n"
        "Или открой в CI/CD после пуша."
    )


async def schedule_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    schedule = load_schedule()
    if not schedule["jobs"]:
        text = (
            "Расписание пусто.\n\n"
            "Добавить автозапуск:\n"
            "/schedule add api daily 09:00\n"
            "/schedule add unit daily 18:00\n"
            "/schedule add all weekly Mon 09:00\n\n"
            "Удалить:\n"
            "/schedule del 0"
        )
    else:
        lines = ["Расписание:\n"]
        for i, job in enumerate(schedule["jobs"]):
            lines.append(f"  {i}. {job['suite']} — {job['freq']} в {job['time']}")
        lines.append("\nДобавить: /schedule add <сьют> daily <HH:MM>")
        lines.append("Удалить: /schedule del <номер>")
        text = "\n".join(lines)

    keyboard = [[InlineKeyboardButton("Назад", callback_data="menu:run")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def schedule_manage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await schedule_cmd(update, context)
        return

    action = context.args[0]

    if action == "add" and len(context.args) >= 4:
        suite = context.args[1]
        freq = context.args[2]
        run_time = context.args[3]

        if suite not in TEST_SUITES and suite != "all":
            await update.message.reply_text(f"Неизвестный сьют: {suite}")
            return

        schedule = load_schedule()
        schedule["jobs"].append({
            "suite": suite,
            "freq": freq,
            "time": run_time,
            "active": True,
        })
        save_schedule(schedule)
        await update.message.reply_text(f"Добавлено: {suite} {freq} в {run_time}")

    elif action == "del" and len(context.args) >= 2:
        try:
            idx = int(context.args[1])
            schedule = load_schedule()
            if 0 <= idx < len(schedule["jobs"]):
                removed = schedule["jobs"].pop(idx)
                save_schedule(schedule)
                await update.message.reply_text(f"Удалено: {removed['suite']} {removed['freq']}")
            else:
                await update.message.reply_text("Неверный номер")
        except ValueError:
            await update.message.reply_text("Укажи номер: /schedule del 0")

    else:
        await update.message.reply_text("Формат: /schedule add <сьют> daily <HH:MM>")


async def run_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Укажи путь:\n/run tests/api/test_api_methods.py"
        )
        return

    path = " ".join(context.args)
    await do_run(update, "custom", path, f"python -m pytest {path} -v --tb=short 2>&1", 60)


# ======================== Запуск тестов ========================

async def do_run(target, suite_key: str, name: str, cmd: str, duration: int):
    if hasattr(target, "message") and target.message:
        msg = await target.message.reply_text(
            f"Запуск: {name}\n{make_progress_bar(0)}\nПодготовка..."
        )
    else:
        msg = await target.edit_message_text(
            f"Запуск: {name}\n{make_progress_bar(0)}\nПодготовка..."
        )

    start_time = time.time()
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=str(PROJECT_ROOT),
    )

    async def progress_loop():
        try:
            while proc.returncode is None:
                elapsed = time.time() - start_time
                pct = min(95, (elapsed / duration) * 100)
                bar = make_progress_bar(pct)
                mins = int(elapsed // 60)
                secs = int(elapsed % 60)
                ts = f"{mins}м {secs}с" if mins else f"{secs}с"
                try:
                    await msg.edit_text(
                        f"Выполняется: {name}\n{bar}\nПрошло: {ts}"
                    )
                except Exception:
                    pass
                await asyncio.sleep(3)
        except asyncio.CancelledError:
            pass

    progress = asyncio.create_task(progress_loop())

    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=duration + 120
        )
    except asyncio.TimeoutError:
        proc.kill()
        stdout, stderr = b"", b""

    progress.cancel()

    out = stdout.decode(errors="replace").strip()
    err = stderr.decode(errors="replace").strip()
    output = f"{out}\n{err}".strip()

    elapsed = time.time() - start_time
    stats = parse_pytest_output(output)

    add_history(
        suite=name,
        passed=stats["passed"],
        failed=stats["failed"],
        errors=stats["errors"],
        elapsed=elapsed,
    )

    result = format_beautiful(proc.returncode, output, name, elapsed)

    keyboard = [
        [InlineKeyboardButton("Заново", callback_data=f"run:{suite_key}")],
        [InlineKeyboardButton("Меню", callback_data="menu:run")],
    ]
    await msg.edit_text(result, reply_markup=InlineKeyboardMarkup(keyboard))


# ======================== Кнопки ========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu:run":
        keyboard = [
            [InlineKeyboardButton("Запустить все", callback_data="run:all")],
            [
                InlineKeyboardButton("API", callback_data="run:api"),
                InlineKeyboardButton("Unit", callback_data="run:unit"),
            ],
            [
                InlineKeyboardButton("UI", callback_data="run:ui"),
                InlineKeyboardButton("Load", callback_data="run:load"),
            ],
            [
                InlineKeyboardButton("API + Unit", callback_data="run:api+unit"),
                InlineKeyboardButton("API + Load", callback_data="run:api+load"),
            ],
            [
                InlineKeyboardButton("История", callback_data="menu:history"),
                InlineKeyboardButton("Расписание", callback_data="menu:schedule"),
            ],
        ]
        await query.edit_message_text(
            "Выбери что запустить:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    if data == "menu:history":
        history = load_history()
        if not history:
            await query.edit_message_text("История пуста.")
            return
        lines = ["Последние запуски:\n"]
        for e in history[:10]:
            icon = "OK" if e["status"] == "OK" else "FAIL"
            lines.append(
                f"{icon} {e['suite']}  {e['passed']}/{e['passed']+e['failed']+e['errors']}  "
                f"{e['elapsed']}с  {e['time']}"
            )
        kb = [[InlineKeyboardButton("Назад", callback_data="menu:run")]]
        await query.edit_message_text("\n".join(lines), reply_markup=InlineKeyboardMarkup(kb))
        return

    if data == "menu:schedule":
        schedule = load_schedule()
        if not schedule["jobs"]:
            text = "Расписание пусто\n\nДобавить: /schedule add api daily 09:00"
        else:
            lines = ["Расписание:\n"]
            for i, j in enumerate(schedule["jobs"]):
                lines.append(f"  {i}. {j['suite']} — {j['freq']} в {j['time']}")
            lines.append("\n/add | /del <номер>")
            text = "\n".join(lines)
        kb = [[InlineKeyboardButton("Назад", callback_data="menu:run")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("run:"):
        suite_key = data.split(":", 1)[1]
        await handle_run(query, suite_key)


async def handle_run(query, suite_key: str):
    if suite_key == "all":
        cmd = "python -m pytest tests/api/ tests/unit/ -v --tb=short 2>&1"
        name = "Все (API + Unit)"
        duration = 60
    elif suite_key in SUITE_GROUPS:
        group = SUITE_GROUPS[suite_key]
        paths = " ".join(TEST_SUITES[s]["path"] for s in group["suites"])
        cmd = f"python -m pytest {paths} -v --tb=short 2>&1"
        name = group["desc"]
        duration = 60
    elif suite_key in TEST_SUITES:
        info = TEST_SUITES[suite_key]
        cmd = f"python -m pytest {info['path']} -v --tb=short 2>&1"
        name = info["desc"]
        duration = 120 if suite_key == "load" else 60
    else:
        await query.edit_message_text(f"Неизвестный сьют: {suite_key}")
        return

    await do_run(query, suite_key, name, cmd, duration)


# ======================== Фоновые задачи ========================

async def schedule_checker(app: Application):
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_day = now.strftime("%A")

        schedule = load_schedule()
        for job in schedule.get("jobs", []):
            if not job.get("active", True):
                continue
            if job["time"] != current_time:
                continue

            freq = job["freq"]
            if freq == "daily" or (freq == "weekly" and job.get("day", "") == current_day):
                suite = job["suite"]
                if suite in TEST_SUITES:
                    info = TEST_SUITES[suite]
                    cmd = f"python -m pytest {info['path']} -v --tb=short 2>&1"
                    name = info["desc"]
                elif suite == "all":
                    cmd = "python -m pytest tests/api/ tests/unit/ -v --tb=short 2>&1"
                    name = "Все (API + Unit)"
                else:
                    continue

                proc = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=str(PROJECT_ROOT),
                )
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=600)
                out = stdout.decode(errors="replace").strip()
                err = stderr.decode(errors="replace").strip()
                output = f"{out}\n{err}".strip()
                stats = parse_pytest_output(output)
                add_history(suite=name, passed=stats["passed"], failed=stats["failed"],
                           errors=stats["errors"], elapsed=0, user="schedule")

        await asyncio.sleep(60)


# ======================== Запуск ========================

def main():
    if not TELEGRAM_TOKEN:
        raise RuntimeError("Set TELEGRAM_TOKEN env var")

    RESULTS_DIR.mkdir(exist_ok=True)

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("suites", suites))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("run", run_custom))
    app.add_handler(CommandHandler("history", history_cmd))
    app.add_handler(CommandHandler("allure", allure_cmd))
    app.add_handler(CommandHandler("schedule", schedule_manage))

    app.add_handler(CallbackQueryHandler(button_handler))

    app.job_queue.run_repeating(schedule_checker, interval=60, first=10)

    print("Бот запущен. Ожидаю команды...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
