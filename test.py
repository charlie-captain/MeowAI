import json
import os

import requests

from src.api import api


def main():
    api.init_var()
    api_pre = 'SYNO.FotoTeam'
    # cookie = os.environ['cookie']
    # token = os.environ['token']
    url = f'{api.base_url}/webapi/entry.cgi/{api_pre}.Browse.Item'
    data = {
        "api": f"{api_pre}.Browse.Item",
        "method": "list",
        "version": "1",
        "offset": 0,
        "limit": -1,
        "additional": '["thumbnail"]',
        "timeline_group_unit": '"day"',
        #     'start_time':,
        # 'end_time':
    }
    # response = requests.post(url, data=data, headers=api.headers)
    # print(response.content)
    total = api.count_total_photos()
    print(total)


if __name__ == '__main__':
    main()
