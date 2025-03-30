import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.models import Worker
from core.logger_setup import log


class CookieWorker(Worker):
    @log.catch
    def __init__(self, ads_data: dict, auth_data: tuple):
        super().__init__(ads_data=ads_data, auth_data=auth_data)

    @log.catch
    def run(self):
        try:
            self.driver.switch_to.window(self.driver.window_handles[0])

            # URL
            self.driver.get(
                'https://www.bitmart.com/voting/en-US')

            # Check authorization
            time.sleep(3)

            try:
                account_img = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="__layout"]/div/div[1]/div/div[2]/span[3]/span/div/div/a/img')))
            except:
                log.warning(f'{self.auth_data[0]} - Аккаунт не авторизован')
                self.driver.quit()
                self.ads_utils.api_ads_browser_action(
                    url=self.close_url)
                return 'Failed_c Не войдено'

            # get cookies
            try:
                access_token = self.driver.get_cookie('accessToken')
                access_salt = self.driver.get_cookie('accessSalt')
            except BaseException as e:
                log.warning(
                    f'{self.auth_data[0]} - Ошибка при получении куки - {e}')
                self.driver.quit()
                self.ads_utils.api_ads_browser_action(url=self.close_url)
                return 'Failed_c Ошибка куки'

            log.success(f'{self.auth_data[0]} - Куки успешно получены!')
            self.driver.quit()
            self.ads_utils.api_ads_browser_action(url=self.close_url)
            return (access_token, access_salt)
        except BaseException as e:
            log.exception(f'{self.auth_data[0]} - Глобальная ошибка - {e}')
            self.driver.quit()
            self.ads_utils.api_ads_browser_action(url=self.close_url)
            return 'Failed_c Global Error'
