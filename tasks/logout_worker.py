import time

from core.bitmart_logout import logout
from core.models import Worker
from core.logger_setup import log


class LogoutWorker(Worker):
    @log.catch
    def __init__(self, ads_data: dict, auth_data: tuple):
        super().__init__(ads_data=ads_data, auth_data=auth_data)

    @log.catch
    def run(self):
        try:
            self.driver.switch_to.window(self.driver.window_handles[0])

            # Check authorization
            old_url = 'https://www.bitmart.com/asset-spot/ru-RU'

            self.driver.get(old_url)

            self.driver.refresh()

            time.sleep(10)
            new_url = self.driver.current_url
            if old_url == new_url:
                access_token = self.driver.get_cookie(
                    'accessToken').get('value')

                result = logout(
                    self.auth_data[0], access_token=access_token)

                if result == False:
                    log.critical(
                        f'{self.auth_data[0]} - Закрываю аккаунт! - Не удалось выйти!')
                    self.driver.quit()
                    self.ads_utils.api_ads_browser_action(
                        url=self.close_url)
                    return 'Failed_l proxy'

                log.success(
                    f'{self.auth_data[0]} - Закрываю аккаунт! - Успешный выход!')
                self.driver.quit()
                self.ads_utils.api_ads_browser_action(
                    url=self.close_url)
                return 'Success_l Успешный выход!'

            log.info(
                f'{self.auth_data[0]} - Закрываю аккаунт! - Не войдено!')
            self.driver.quit()
            self.ads_utils.api_ads_browser_action(
                url=self.close_url)
            return 'Success_l Не войдено!'
        except Exception as e:
            log.info(
                f'{self.auth_data[0]} - Глобальная ошибка! - {e}')
            self.driver.quit()
            self.ads_utils.api_ads_browser_action(
                url=self.close_url)
            return 'Failed_l Глобальная ошибка!'
