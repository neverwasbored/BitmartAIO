import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from config import Config
from core.ads_utils import Ads
from core.selenium_utils import close_all_windows
from core.logger_setup import log


class Worker():
    @log.catch
    def __init__(self, ads_data: dict, auth_data: tuple):
        self.ads_utils = Ads()
        self.auth_data = auth_data
        user_id = ads_data.get('user_id')

        self.open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + user_id
        self.close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + user_id

        response = self.ads_utils.api_ads_browser_action(url=self.open_url)

        chrome_driver = response["data"]["webdriver"]
        service = Service(executable_path=chrome_driver,
                          log_output=f'logs_webdriver/{auth_data[0]}.log')

        chrome_options = Options()
        chrome_options.add_experimental_option(
            "debuggerAddress", response["data"]["ws"]["selenium"])
        # chrome_options.add_argument('--headless=new')

        self.driver = webdriver.Chrome(
            service=service, options=chrome_options)

        if Config.FULL_SCREEN == True:
            try:
                self.driver.maximize_window()
            except:
                log.warning(
                    'Ошибка при дествии открытия окна на весь экран. Вероятно оно уже во весь экран!')

        if len(self.driver.window_handles) > 1:
            close_all_windows(driver=self.driver)

        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(5)

    def run(self):
        pass
