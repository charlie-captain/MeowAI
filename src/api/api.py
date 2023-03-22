import json
import os
import socket

import requests

from src.detect.detect import detect
from src.log.logger import logger

base_url = 'http://127.0.0.1:5000'
cookie = None
token = None
headers = {
    'Cookie': cookie,
    'X-SYNO-TOKEN': token,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

tags = []
offset = 0
limit = 1000

done_list = []


def get_tags():
    url = f'{base_url}/webapi/entry.cgi/SYNO.FotoTeam.Browse.GeneralTag'
    data = {
        'api': 'SYNO.FotoTeam.Browse.GeneralTag',
        'method': 'list',
        'version': '1',
        'limit': '500',
        'offset': '0'
    }
    response = requests.post(url, data, headers=headers)
    data = json.loads(response.content)
    if data['success']:
        list = data['data']['list']
        return list
    return []


def get_time_line():
    url = f'{base_url}/webapi/entry.cgi/SYNO.FotoTeam.Browse.Timeline'
    data = {
        'api': 'SYNO.FotoTeam.Browse.Timeline',
        'method': 'get',
        'version': '2',
        'timeline_group_unit': 'day'
    }
    response = requests.post(url, data, headers=headers)
    data = json.loads(response.content)
    if data['success']:
        section_list = data['data']['section']


def start_indexing():
    global offset
    has_more = True
    while (has_more):
        has_more = get_photos()
        if not has_more:
            break
        offset += limit


def get_photos():
    global url, data
    logger.info(f'current offset = {offset} limit = {limit}')
    url = f'{base_url}/webapi/entry.cgi/SYNO.FotoTeam.Browse.Item'
    data = {
        "api": "SYNO.FotoTeam.Browse.Item",
        "method": "list",
        "version": "1",
        "offset": offset,
        "limit": limit,
        "additional": '["thumbnail"]',
        "timeline_group_unit": '"day"',
        #     'start_time':,
        # 'end_time':
    }

    response = requests.post(url, data=data, headers=headers)
    data = json.loads(response.content)
    # print(data)
    if data['success']:
        list = data['data']['list']
        logger.info(f'get_photos: {len(list)}')
        for p in list:
            id = p['id']
            if has_done(id):
                continue
            thumbnail = p['additional']['thumbnail']
            cache_key = thumbnail['cache_key']
            image_content = get_photo_by_id(id, cache_key, headers)
            is_detect = detect_image(image_content)
            logger.debug(f'{id} {cache_key} {is_detect}')
            if is_detect:
                bind_tag(id, tag_name='猫')
        add_to_done_list(list)
        return True
    else:
        logger.info(response.content)
        return False


def detect_image(image_content):
    is_cat = detect(image_content)
    if is_cat:
        return True
    else:
        return False


def get_photo_by_id(id, cache_key, headers):
    # print(f'{id}  {cache_key}')
    url = f'{base_url}/webapi/entry.cgi?id={id}&cache_key={cache_key}&type=unit&size=sm&api=SYNO.FotoTeam.Thumbnail&method=get&version=2&SynoToken=NXibb.RkEVsCY'
    # print(url)
    headers[
        'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    headers['Accept-Encoding'] = 'gzip, deflate'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        print(response.content)
    return False


def create_tag(tag_name):
    url = f'{base_url}/webapi/entry.cgi/SYNO.FotoTeam.Browse.GeneralTag'
    data = {
        'api': 'SYNO.FotoTeam.Browse.GeneralTag',
        'method': 'create',
        'version': '1',
        'name': tag_name,
    }
    response = requests.post(url, data, headers=headers)
    data = json.loads(response.content)
    if data['success']:
        print('标签添加成功')
        tags.append(data['data']['tag'])
    else:
        print('标签添加失败')


def bind_tag(id, tag_name):
    tag_id = get_tag_id_by_name(tag_name)

    if tag_id is None:
        create_tag(tag_name)
        tag_id = get_tag_id_by_name(tag_name)

    url = f'{base_url}/webapi/entry.cgi/SYNO.FotoTeam.Browse.Item'
    data = {
        'api': 'SYNO.FotoTeam.Browse.Item',
        'method': 'add_tag',
        'version': '1',
        'id': f'[{id}]',
        'tag': f'[{tag_id}]'
    }
    # print(data)
    response = requests.post(url, data, headers=headers)
    data = json.loads(response.content)
    if data['success']:
        print('绑定标签成功')
        return True
    else:
        print('添加标签失败')
        return False


def get_tag_id_by_name(tag_name):
    for tag in tags:
        if tag['name'] == tag_name:
            return tag['id']
    return None


def read_done_list():
    try:
        done_list_file = get_done_list_file_path()
        with open(done_list_file, 'r') as f:
            data = json.load(f)
        global done_list
        done_list = data
    except FileNotFoundError:
        os.mknod(done_list_file)
        print("文件创建成功！")
    except Exception as e:
        logger.error(e)


def get_done_list_file_path():
    root_path = os.path.abspath(os.getcwd())
    done_list_file = os.path.join(root_path, 'done_list.json')
    return done_list_file


def has_done(id):
    for d in done_list:
        if d['id'] == id:
            return True
    return False


def add_to_done_list(list):
    for done in list:
        done_list.append(done)
    with open(get_done_list_file_path(), 'w') as f:
        json.dump(done_list, f)


def start():
    global cookie
    global token
    cookie = os.environ.get('cookie')
    token = os.environ.get('token')
    read_done_list()
    global tags
    tags = get_tags()
    print(tags)
    start_indexing()


if __name__ == '__main__':
    start_indexing()
