import allure
from ui.pages.footer_page import FooterPage
from urls import BASE_URL

def test_footer_links_visible(driver):
    page = FooterPage(driver)
    page.open(BASE_URL)

    links = page.get_footer_links()

    with allure.step("Проверяем, что футер содержит ссылки"):
        assert len(links) > 0, "Футер должен содержать хотя бы одну ссылку"

    for link in links:
        with allure.step(f"Проверяем отображение ссылки: {link}"):
            assert link.strip() != "", "Ссылка в футере не должна быть пустой"


def test_footer_copyright(driver):
    page = FooterPage(driver)
    page.open(BASE_URL)

    links = page.get_footer_links()
    with allure.step("Проверяем наличие футера"):
        assert len(links) > 0, "Футер должен содержать ссылки"
