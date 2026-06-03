import pytest
import allure
import requests


@allure.feature('Тест с параметризацией')
@allure.story('Проверка статус кода')
class TestApiV1Activities:
    @pytest.mark.parametrize('status_code, name_site, url', [
        (200, "Skip to content", "https://www.whitehouse.gov/#wp--skip-link--target"),
        (200, "", "https://www.whitehouse.gov/"),
        (200, "Investments", "https://www.whitehouse.gov/investments/"),
        (200, "SAVE America", "https://www.whitehouse.gov/saveamerica/"),
        (200, "Contact", "https://www.whitehouse.gov/contact/"),
        (200, "Gallery", "https://www.whitehouse.gov/gallery/"),
        (200, "News", "https://www.whitehouse.gov/news/"),
        (200, "Livestream", "https://www.whitehouse.gov/live/"),
        (403, "Trump Accounts", "https://trumpaccounts.gov/"),
        (200, "Releases", "https://www.whitehouse.gov/releases/"),
        (200, "Lab Leak: The True O", "https://www.whitehouse.gov/lab-leak-true-origins-of-covid-19/"),
        (200, "January 6: A Date Wh", "https://www.whitehouse.gov/j6/"),
        (200, "This Is Our Why", "https://www.whitehouse.gov/why/"),
        (200, "The JFK Files", "https://www.whitehouse.gov/jfk-files/"),
        (200, "The RFK Files", "https://www.whitehouse.gov/rfk-files/"),
        (200, "Criminal Aliens Rece", "https://www.whitehouse.gov/criminals/"),
        (200, "Briefings & Statemen", "https://www.whitehouse.gov/briefings-statements/"),
        (200, "Fact Sheets", "https://www.whitehouse.gov/fact-sheets/"),
        (200, "Presidential Actions", "https://www.whitehouse.gov/presidential-actions/"),
        (200, "Arrested: Worst of t", "https://www.dhs.gov/wow"),
        (200, "Photo Gallery", "https://www.whitehouse.gov/gallery/"),
        (200, "Executive Orders", "https://www.whitehouse.gov/presidential-actions/executive-orders/"),
        (200, "Presidential Memoran", "https://www.whitehouse.gov/presidential-actions/presidential-memoranda/"),
        (200, "Remarks", "https://www.whitehouse.gov/remarks/"),
        (200, "Nominations & Appoin", "https://www.whitehouse.gov/presidential-actions/nominations-appointments/"),
        (200, "Proclamations", "https://www.whitehouse.gov/presidential-actions/proclamations/"),
        (200, "Research", "https://www.whitehouse.gov/research/"),
        (200, "Administration", "https://www.whitehouse.gov/administration/"),
        (200, "President Donald J. ", "https://www.whitehouse.gov/administration/donald-j-trump/"),
        (200, "First Lady Melania T", "https://www.whitehouse.gov/administration/melania-trump/"),
        (200, "Vice President JD Va", "https://www.whitehouse.gov/administration/jd-vance/"),
        (200, "Second Lady Usha Van", "https://www.whitehouse.gov/administration/usha-vance/"),
        (200, "The Cabinet", "https://www.whitehouse.gov/administration/cabinet/"),
        (200, "Livestream", "https://www.whitehouse.gov/live/"),
        (200, "Video Library", "https://www.whitehouse.gov/videos/"),
        (200, "White House Wire", "https://www.whitehouse.gov/wire/"),
        (200, "Media Offenders", "https://www.whitehouse.gov/mediabias/"),
        (200, "Protect Religious Li", "https://www.whitehouse.gov/priorities/faith/"),
        (200, "Unleash American Ene", "https://www.whitehouse.gov/priorities/energy/"),
        (200, "The SAVE America Act", "https://www.whitehouse.gov/saveamerica/"),
        (200, "School Choice", "https://www.whitehouse.gov/schoolchoice/"),
        (200, "Crypto", "https://www.whitehouse.gov/crypto/"),
        (200, "Fostering the Future", "https://www.whitehouse.gov/fosteringthefuture/"),
        (200, "The Great Healthcare", "https://www.whitehouse.gov/greathealthcare/"),
        (200, "AI.Gov", "https://www.ai.gov/"),
        (200, "The Trump Gold Card", "https://www.trumpcard.gov/"),
        (200, "TrumpRx", "https://trumprx.gov/")
    ])
    @allure.title('Проверка статус кода страниц на экране main')
    def test_api_v1_activities(self, status_code, name_site, url):
        with allure.step('Вызов ручки /api/v1/Activities/'):
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'max-age=0',
                'priority': 'u=0, i',
                'referer': 'https://www.whitehouse.gov/',
                'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'
            }
            response = requests.get(url=url, headers=headers)

            with allure.step(f'Проверка стутс кода страницы {name_site}'):
                assert response.status_code == status_code