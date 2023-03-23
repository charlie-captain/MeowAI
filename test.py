import os

import requests


def main():
    base_url='http://127.0.0.1:5000'
    api_pre = 'SYNO.FotoTeam'
    cookie = os.environ['cookie']
    token = os.environ['token']
    headers = {
        'Cookie': cookie,
        'X-SYNO-TOKEN':token ,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    url = f'{base_url}/webapi/entry.cgi/SYNO.FotoTeam.Browse.GeneralTag'
    data = {
        'api': f'SYNO.FotoTeam.Browse.GeneralTag',
        'method': 'list',
        'version': '1',
        'limit': '500',
        'offset': '0'
    }
    response = requests.post(url, data, headers=headers)
    print(response.content)
    url = f'{base_url}/webapi/entry.cgi/{api_pre}.Browse.Item'
    data = {
        "api": f"{api_pre}.Browse.Item",
        "method": "list",
        "version": "1",
        "offset": 0,
        "limit": 10,
        "additional": '["thumbnail"]',
        "timeline_group_unit": '"day"',
        #     'start_time':,
        # 'end_time':
    }
    response = requests.post(url, data=data, headers=headers)
    print(response.content)


if __name__ == '__main__':
    main()
