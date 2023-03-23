import json
import os

import requests


def main():
    url = ''
    response = requests.get(url)
    print(response.content)
    print(response.headers)
    base_url = 'http://127.0.0.1:5000'
    api_pre = 'SYNO.FotoTeam'
    # cookie = os.environ['cookie']
    # token = os.environ['token']
    data = json.loads(response.content)
    cookie = response.headers.get('Set-Cookie')
    token = data['data']['synotoken']
    headers = {
        'Cookie': cookie,
        'X-SYNO-TOKEN': token,
    }
    print(headers)
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
