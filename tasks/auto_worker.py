import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from core.pyotp_utils import Authenticator
from core.models import Worker
from config import AutoConfig
from core.logger_setup import log


class AutoWorker(Worker):
    @log.catch
    def __init__(self, ads_data: dict, auth_data: tuple):
        super().__init__(ads_data=ads_data, auth_data=auth_data)
        self.authenticator = Authenticator(self.auth_data[3])

    @log.catch
    def run(self):
        try:
            wait = WebDriverWait(self.driver, 30)

            retrys = 0

            # Check authorization
            old_url = 'https://www.bitmart.com/asset-spot/ru-RU'

            self.driver.get(
                'https://www.bitmart.com/asset-spot/ru-RU')

            time.sleep(10)
            new_url = self.driver.current_url

            if old_url == new_url:
                log.info(f'{self.auth_data[0]} - Уже войдено!')
                self.driver.quit()
                self.ads_utils.api_ads_browser_action(
                    url=self.close_url)
                return 'Success_a Уже войдено!'

            # delete cookies and cache
            # self.driver.delete_all_cookies()
            self.driver.execute_script(
                "window.caches.keys().then(keys => { keys.forEach(key => { window.caches.delete(key); }) });")
            time.sleep(2)

            # Account cicle
            while True:
                if retrys == AutoConfig.RETRYS_COUNT:
                    try:
                        log.warning(
                            f'{self.auth_data[0]} - Код не смог выполниться за {retrys} попыток...')
                        self.driver.quit()
                        self.ads_utils.api_ads_browser_action(
                            url=self.close_url)
                    except:
                        pass
                    return f'Failed_a Неудача за {retrys} попыток'

                retrys += 1

                # URL
                original_url = 'https://www.bitmart.com/login/en-US'

                self.driver.get('https://www.bitmart.com/login/en-US')

                # Input data
                try:
                    log.debug(
                        f'{self.auth_data[0]} - Вхожу по данным - {self.auth_data[1]}:{self.auth_data[2]} Попытка: {retrys}')

                    new_url = self.driver.current_url
                    if original_url != new_url:
                        self.driver.get('https://www.bitmart.com/login/en-US')
                    self.auth()
                except BaseException as e:
                    log.exception(
                        f'{self.auth_data[0]} - Ошибка при вводе данных! - {e}')
                    self.driver.quit()
                    self.ads_utils.api_ads_browser_action(
                        url=self.close_url)
                    return f'Failed_a Input data Error'

                # input google 2fa
                try:
                    try:
                        input_google_authenticator = WebDriverWait(self.driver, AutoConfig.WAIT_CAPTCHA).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div[4]/input')))
                        self.authenticator.get_2fa_code(
                            input_google_authenticator)
                    except:
                        try:
                            input_google_authenticator = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                                (By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/div[4]/input')))
                            self.authenticator.get_2fa_code(
                                input_google_authenticator)
                            time.sleep(2)
                            confirm_btn = wait.until(EC.element_to_be_clickable(
                                (By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div/div[2]/div[2]/button')))
                            confirm_btn.click()
                        except:
                            continue
                except BaseException as e:
                    log.exception(
                        f'{self.auth_data[0]} - Ошибка ввода 2fa или неверное решение капчи - {e}')
                    self.driver.quit()
                    self.ads_utils.api_ads_browser_action(
                        url=self.close_url)
                    return f'Failed_a Input google 2fa Error'

                time.sleep(7)
                log.debug(f'{self.auth_data[0]} - Успешный вход!')

                # Success
                self.driver.quit()
                self.ads_utils.api_ads_browser_action(
                    url=self.close_url)
                return 'Success_a'
        except BaseException as e:
            log.exception(
                f'{self.auth_data[0]} - Глобальная ошибка - {e}')
            self.driver.quit()
            self.ads_utils.api_ads_browser_action(
                url=self.close_url)
            return f'Failed_a Global Error'

    def auth(self):
        wait = WebDriverWait(self.driver, 30)
        email_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/form/div[1]/div/div[1]/div/input')))
        email_input.send_keys(self.auth_data[1])
        password_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/form/div[2]/div/div/span/span/div/input')))
        password_input.send_keys(self.auth_data[2])
        time.sleep(2)
        sign_in_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/form/div[3]/div/button')))
        sign_in_btn.click()
        time.sleep(8)
