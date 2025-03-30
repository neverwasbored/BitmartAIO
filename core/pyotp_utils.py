import datetime
import time

import pyotp
from core.logger_setup import log


class Authenticator:
    @log.catch
    def __init__(self, auth_code: str):
        self.auth_code = auth_code
        self.totp = pyotp.TOTP(self.auth_code)

    @log.catch
    def generate_totp_code(self) -> str:
        return self.totp.now()

    @log.catch
    def get_expires_time(self):
        return self.totp.interval - datetime.datetime.now().timestamp() % self.totp.interval

    @log.catch
    def is_available(self):
        if self.get_expires_time() < 5:
            return False
        return True

    @log.catch
    def get_2fa_code(self, input_google_authenticator):
        while True:
            if self.is_available() == False:
                time.sleep(1)
                continue
            input_google_authenticator.send_keys(
                self.generate_totp_code())
            break
        return True
