import requests
from core.db_utils import DataBase

db = DataBase()


def logout(serial_number: str | int, access_token: str) -> bool:
    proxy = db.get_db_proxy(serial_number=serial_number).split(':')

    if not proxy:
        return False

    proxies = {
        "http": f'socks5://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}',
        "https": f'socks5://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}',
    }

    check_proxy_res = check_proxy(proxy=proxy, proxies=proxies)
    if not check_proxy_res:
        return False

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru',
        'authorization': access_token,
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'expires': '0',
        'origin': 'https://www.bitmart.com',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Chromium";v="100", "Google Chrome";v="100", "Not(A:Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
        'x-bm-client': 'WEB',
        'x-bm-ua': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
    }

    data = {
        'token': access_token
    }
    try:
        response = requests.post(url='https://www.bitmart.com/gw-api/user-center/token/logout',
                                 proxies=proxies,
                                 headers=headers,
                                 data=data)
        if response.status_code == 200 and response.json().get('msg') == 'Success':
            return True
        return False
    except:
        return False


def check_proxy(proxy: list, proxies: dict) -> bool:
    try:
        ip = requests.get('http://eth0.me/', proxies=proxies,
                          timeout=10).text.rstrip()

        if ip not in proxy:
            return False
        return True
    except requests.RequestException:
        return False
