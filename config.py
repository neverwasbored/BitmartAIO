class Config:
    API_URL: str = 'http://local.adspower.net:50325'
    API_KEY: str = 'Your_Ads_Api_Key'
    GROUP_LIST: list[str] = ['BM3']  # 'BM1', 'BM2', 'BM3'
    DB_NAME: str = 'accounts.db'  # Название базы данных
    LOGS_TIME: int = 7  # Сколько дней будет хранится файл логов. Работает только при 'a'
    LOGS_MODE: str = 'a'  # 'a' - добавление в файл логов | 'w' - очистка при каждом запуске
    FULL_SCREEN: bool = False  # Открытие всех браузеров в режиме FULL_SCREEN


class AutoConfig(Config):
    PROCESS_COUNT: int = 25  # Максимальное количество процессов
    RETRYS_COUNT = 3  # Количество попыток входа в аккаунт
    WAIT_CAPTCHA = 90  # Количество секунд которое код будет ждать капчу
    # LOGOUT_IF_SIGNED: bool = False  # Выходить из аккаунта если уже войдено


class CookieConfig(Config):
    PROCESS_COUNT: int = 25  # Максимальное количество процессов
    CLEAN_UP_TXT: bool = True  # Очистка файлов txt при каждом запуске при сборе всех куки
    # LOGIN_IF_NOT: bool = False  # Входить на аккаунт если не войден


class LogoutConfig(Config):
    PROCESS_COUNT: int = 25  # Максимальное количество процессов
