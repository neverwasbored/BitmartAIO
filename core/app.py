import time
import json
from concurrent.futures import ProcessPoolExecutor

from config import *
from core.ads_utils import Ads
from core.db_utils import DataBase
from core.models import Worker
from core.txt_utils import clean_up_txt, logs_txt
from tasks import auto_worker, cookie_worker, logout_worker
from core.logger_setup import log


class App:
    @log.catch
    def __init__(self):
        self.ads_utils = Ads()
        self.data_base_utils = DataBase()

    @log.catch
    def mode_choise(self) -> int:
        if not self.ads_utils.connection_status():
            raise ConnectionError('Connection error. Try to open adspower.')

        print('''
            -------------------Bitmart Logout-------------------
            1. Выйти из всех аккаунтов.
            2. Выйти из аккаунтов, из которых не удалось выйти.
              
            -------------------BITMART   AUTO-------------------
            3. Войти во все аккаунты.
            4. Войти в аккаунты, в которые не удалось войти.
              
            -------------------BITMART COOKIE-------------------
            5. Собрать куки со всех аккаунтов.
            6. Собрать куки, которые не удалось собрать.
              ''')
        your_choise = input('Введите цифру - ваш выбор: ')
        if your_choise not in ['1', '2', '3', '4', '5', '6']:
            raise ValueError(
                'Ошибка ввода. Результат должен быть 0, 1, 2, 3 или 4')
        self.mode = int(your_choise)

        start_time = int(time.time())

        self.run()

        end_time = int(time.time())
        log.info(f'Выполнение кода заняло: {end_time - start_time} секунд!')

    @log.catch
    def run(self):
        log.info('Успешный запуск кода!')

        self.ads_data = self.ads_utils.get_serial_numbers_by_group_name()

        if self.mode == 1:
            log.info(
                f'Bitmart Logout: Произвожу выход со всех аккаунтов из групп: {Config.GROUP_LIST}!')

            self.auth_data = self.data_base_utils.get_db_data_logout()
            self.multi_processing(config=LogoutConfig,
                                  worker=logout_worker.LogoutWorker)

            failed_accs = len(
                self.data_base_utils.get_db_fail_accounts_logout())
            log.info(f'Количество неудач: {failed_accs}')

        if self.mode == 2:
            log.info(
                f'Bitmart Logout: Произвожу выход из аккаунтов, из которых не удалось выйти: {Config.GROUP_LIST}!')

            self.auth_data = self.data_base_utils.get_db_fail_accounts_logout()
            self.multi_processing(config=LogoutConfig,
                                  worker=logout_worker.LogoutWorker)
            failed_accs = len(
                self.data_base_utils.get_db_fail_accounts_logout())
            log.info(f'Количество неудач: {failed_accs}')

        if self.mode == 3:
            log.info(
                f'Bitmart Auto: Начинаю входить во все аккаунты из групп: {Config.GROUP_LIST}!')

            self.auth_data = self.data_base_utils.get_db_data_auto()
            self.multi_processing(config=AutoConfig,
                                  worker=auto_worker.AutoWorker)

            failed_accs = len(self.data_base_utils.get_db_fail_accounts_auto())
            log.info(f'Количество неудач: {failed_accs}')

        if self.mode == 4:
            log.info(
                f'Bitmart Auto: Начинаю входить в аккаунты, в которые не удалось войти!')

            self.auth_data = self.data_base_utils.get_db_fail_accounts_auto()

            if len(self.auth_data) == 0:
                log.info(f'Нет не выполненных аккаунтов!')
                return

            self.multi_processing(config=AutoConfig,
                                  worker=auto_worker.AutoWorker)
            failed_accs = len(self.data_base_utils.get_db_fail_accounts_auto())
            log.info(f'Количество неудач: {failed_accs}')

        if self.mode == 5:
            log.info(
                f'Bitmart Cookie: Начинаю собирать куки со всех аккаунтов!')

            if CookieConfig.CLEAN_UP_TXT == True:
                clean_up_txt()

            self.auth_data = self.data_base_utils.get_db_data_cookie()
            self.multi_processing(config=CookieConfig,
                                  worker=cookie_worker.CookieWorker)

            failed_accs = len(
                self.data_base_utils.get_db_fail_accounts_cookie())
            log.info(f'Количество неудач: {failed_accs}')

        if self.mode == 6:
            log.info(
                f'Bitmart Cookie: Начинаю собирать куки, которые не удалось собрать!')

            self.auth_data = self.data_base_utils.get_db_fail_accounts_cookie()

            if len(self.auth_data) == 0:
                log.info(f'Нет не выполненных аккаунтов!')
                return

            self.multi_processing(config=CookieConfig,
                                  worker=cookie_worker.CookieWorker)
            failed_accs = len(
                self.data_base_utils.get_db_fail_accounts_cookie())
            log.info(f'Количество неудач: {failed_accs}')

    @log.catch
    def multi_processing(self, config: Config, worker: Worker):
        with ProcessPoolExecutor(max_workers=config.PROCESS_COUNT) as executor:
            futures = []
            for elem in self.ads_data:
                for account in self.auth_data:
                    if int(elem.get('serial_number')) == account[0]:
                        futures.append(executor.submit(
                            self.worker_process, worker, elem, account))
                        break

            for future in futures:
                future.result()

    @log.catch
    def worker_process(self, worker: Worker, elem: dict, account: tuple):
        log.info(f'{account[0]} - Запускаюсь!')

        worker = worker(ads_data=elem, auth_data=account)

        result = worker.run()

        self.check_result(result=result, account=account)
        log.info(f'{account[0]} - Завершаюсь!')

    @log.catch
    def check_result(self, result: tuple | str, account: tuple):
        if isinstance(result, tuple):
            log.debug(f'{account[0]} - Получил кортеж куки')
            proxy_split = account[1].split(':')
            vote_data = {
                "proxy": f"http://{proxy_split[2]}:{proxy_split[3]}@{proxy_split[0]}:1050",
                "account": {
                    "accessToken": result[0].get('value'),
                    "accessSalt": result[1].get('value')
                }
            }

            text = json.dumps(vote_data)
            log.debug(
                f'{account[0]} - Переобразовал строку в нужный формат')

            logs_txt(mode=1, text=str(text), serial_number=account[0])
            logs_txt(mode=2, text=text)
            log.success(f'{account[0]} - Успех!')
            self.data_base_utils.db_result(
                column='cookie_result',
                account=account,
                text='Success_c'
            )

        elif 'Failed_c' in result:
            log.warning(f'{account[0]} - Ошибка! - {result}')
            self.data_base_utils.db_result(
                column='cookie_result',
                account=account,
                text=result
            )
            if 'Не войдено' in result:
                self.data_base_utils.db_result(
                    column='auto_result',
                    account=account,
                    text='Failed_a Не войдено при сборе куки!'
                )

        elif 'Success_a' in result:
            log.success(f'{account[0]} - Успешно!')
            self.data_base_utils.db_result(
                column='auto_result',
                account=account,
                text=f'{result} Успех!'
            )

        elif 'Failed_a' in result:
            log.warning(f'{account[0]} - Ошибка! - {result}')
            self.data_base_utils.db_result(
                column='auto_result',
                account=account,
                text=result
            )

        elif 'Success_l' in result:
            log.success(f'{account[0]} - Успешно!')
            self.data_base_utils.db_result(
                column='logout_result',
                account=account,
                text=result
            )

        elif 'Failed_l' in result:
            log.warning(f'{account[0]} - Ошибка! - {result}')
            self.data_base_utils.db_result(
                column='logout_result',
                account=account,
                text=result
            )
