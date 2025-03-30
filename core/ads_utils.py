import time
import random

import requests

from config import Config


config = Config()


class Ads:
    def connection_status(self) -> bool:
        try:
            response = requests.get(f'{config.API_URL}/status').json()
            if response.get('msg') == 'success':
                return True
            return False
        except:
            return False

    def get_user_list(self) -> list:
        response_list = []
        for elem in range(1, 3):
            params = {
                'page_size': 1000,
                'page': elem
            }

            response = requests.get(
                f'{config.API_URL}/api/v1/user/list', params=params).json().get('data').get('list')
            response_list += response
            time.sleep(2)
        return response

    def get_serial_numbers_by_group_name(self) -> list:
        if len(config.GROUP_LIST) == 0:
            raise 'Введите хотя бы одну группу!'
        serial_numbers = []
        user_list = self.get_user_list()
        for elem in user_list:
            temp_dict = {}
            for group in config.GROUP_LIST:
                if elem.get('group_name') == group:
                    temp_dict['serial_number'] = elem.get('serial_number')
                    temp_dict['user_id'] = elem.get('user_id')
                    serial_numbers.append(temp_dict)
        return serial_numbers

    def api_ads_browser_action(self, url: str = None):
        response = requests.get(url).json()
        if self.connection_queue_status(response=response) == False:
            while True:
                time.sleep(random.randint(1, 5))
                response = requests.get(url).json()
                if self.connection_queue_status(response=response) == False:
                    continue
                break
        return response

    @staticmethod
    def connection_queue_status(response) -> bool:
        if response["code"] != 0:
            return False
        return True
