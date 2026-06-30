import pytest
import allure
import subprocess
import csv
import os
import tempfile

LOCUSTFILE = os.path.join(os.path.dirname(__file__), "locustfile.py")
BASE_URL = "https://www.whitehouse.gov"


@allure.feature("Load Testing")
@allure.story("Locust performance tests")
class TestLoad:
    MAX_AVG_MS = 5000
    MIN_REQUESTS = 5

    @allure.title("GET load — 5 users, 15s")
    def test_get_load(self):
        results = self._run("GetRequestsUser", duration=15, users=5)

        with allure.step("Validate"):
            self._attach(results, "GET Load")
            assert results["total"] >= self.MIN_REQUESTS, \
                f"Too few requests: {results['total']}"
            assert results["avg_ms"] < self.MAX_AVG_MS, \
                f"Avg {results['avg_ms']:.0f}ms > {self.MAX_AVG_MS}ms"

    @allure.title("POST load — 3 users, 10s")
    def test_post_load(self):
        results = self._run("PostRequestsUser", duration=10, users=3)

        with allure.step("Validate"):
            self._attach(results, "POST Load")
            assert results["total"] >= 1

    @allure.title("PUT load — 3 users, 10s")
    def test_put_load(self):
        results = self._run("PutRequestsUser", duration=10, users=3)

        with allure.step("Validate"):
            self._attach(results, "PUT Load")
            assert results["total"] >= 1

    @allure.title("PATCH load — 3 users, 10s")
    def test_patch_load(self):
        results = self._run("PatchRequestsUser", duration=10, users=3)

        with allure.step("Validate"):
            self._attach(results, "PATCH Load")
            assert results["total"] >= 1

    @allure.title("Stress — 15 users, 20s")
    def test_stress(self):
        results = self._run("GetRequestsUser", duration=20, users=15)

        with allure.step("Validate"):
            self._attach(results, "Stress")
            assert results["total"] >= self.MIN_REQUESTS * 3
            assert results["avg_ms"] < self.MAX_AVG_MS * 2

    @allure.title("Spike — all classes mixed, 10 users, 15s")
    def test_spike(self):
        classes = "GetRequestsUser PostRequestsUser PutRequestsUser PatchRequestsUser"
        results = self._run(classes, duration=15, users=10)

        with allure.step("Validate"):
            self._attach(results, "Spike")
            assert results["total"] >= self.MIN_REQUESTS * 2

    def _run(self, user_classes, duration, users):
        tmpdir = tempfile.mkdtemp()
        csv_prefix = os.path.join(tmpdir, "stats")

        cmd = [
            "locust",
            "-f", LOCUSTFILE,
            "--headless",
            "-u", str(users),
            "-r", str(min(users, 5)),
            "--run-time", f"{duration}s",
            "--host", BASE_URL,
            "--csv", csv_prefix,
            "--only-summary",
        ]
        cmd.extend(user_classes.split())

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=duration + 60,
            cwd=os.path.dirname(LOCUSTFILE),
        )

        stats_path = csv_prefix + "_stats.csv"
        if not os.path.exists(stats_path):
            # Locust may write CSV relative to -f file location
            fallback = os.path.join(os.path.dirname(LOCUSTFILE), "stats_stats.csv")
            if os.path.exists(fallback):
                import shutil
                shutil.copy(fallback, stats_path)
                os.remove(fallback)
                for f in ["stats_exceptions.csv", "stats_failures.csv", "stats_stats_history.csv"]:
                    p = os.path.join(os.path.dirname(LOCUSTFILE), f)
                    if os.path.exists(p):
                        os.remove(p)

        if not os.path.exists(stats_path):
            print(f"DEBUG: proc.returncode={proc.returncode}")
            print(f"DEBUG: stderr={proc.stderr[-200:]}")
            print(f"DEBUG: csv_prefix={csv_prefix}")
            print(f"DEBUG: tmpdir={tmpdir}")
            print(f"DEBUG: files={os.listdir(tmpdir) if os.path.exists(tmpdir) else 'N/A'}")

        return self._parse(csv_prefix)

    def _parse(self, csv_prefix):
        path = csv_prefix + "_stats.csv"
        empty = {"total": 0, "avg_ms": 0, "max_ms": 0, "failed": 0, "rps": 0, "endpoints": {}}

        if not os.path.exists(path):
            return empty

        total = 0
        avg_ms = 0.0
        max_ms = 0.0
        failed = 0
        rps = 0.0
        endpoints = {}

        with open(path, "r") as f:
            for row in csv.DictReader(f):
                tp = row.get("Type", "")
                name = row.get("Name", "")

                if name == "Aggregated" or tp == "Aggregated":
                    total = int(row.get("Request Count", 0))
                    failed = int(row.get("Failure Count", 0))
                    avg_ms = float(row.get("Average Response Time", 0))
                    rps = float(row.get("Requests/s", 0))
                elif name and name != "Aggregated":
                    ep_max = float(row.get("99%", 0))
                    endpoints[name] = {
                        "count": int(row.get("Request Count", 0)),
                        "avg": float(row.get("Average Response Time", 0)),
                        "max": ep_max,
                    }
                    if ep_max > max_ms:
                        max_ms = ep_max

        return {"total": total, "avg_ms": avg_ms, "max_ms": max_ms,
                "failed": failed, "rps": rps, "endpoints": endpoints}

    def _attach(self, r, title):
        lines = [
            f"Total requests: {r['total']}",
            f"Avg response time: {r['avg_ms']:.0f}ms",
            f"Max response time: {r['max_ms']:.0f}ms",
            f"Failed requests: {r['failed']}",
            f"RPS: {r['rps']:.1f}",
        ]
        if r["endpoints"]:
            lines.append("\nPer endpoint:")
            for ep, d in r["endpoints"].items():
                lines.append(f"  {ep}: {d['count']} reqs, avg {d['avg']:.0f}ms, p99 {d['max']:.0f}ms")

        allure.attach("\n".join(lines), name=f"{title} Results",
                      attachment_type=allure.attachment_type.TEXT)
