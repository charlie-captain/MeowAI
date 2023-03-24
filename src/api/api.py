import json
import os

import requests
from tqdm import tqdm

from src.detect.detect import detect
from src.log import logger as log
from src.log.logger import logger

base_url = 'http://127.0.0.1:5000'
cookie = None
token = None
headers = None
tags = []
offset = 0
limit = 1000
done_list = []
# 识别文件夹
mode = 'person'
# api 前缀
api_pre = None
# 识别成功列表
detect_list = []
username = None
pwd = None
token_error_code = ['119', '120', '150']


def get_token():
    global cookie
    global token
    global headers
    url = f'{base_url}/photo/webapi/auth.cgi?api=SYNO.API.Auth&version=3&method=login&account={username}&passwd={pwd}&enable_syno_token=yes'
    response = requests.get(url)
    try:
        data = json.loads(response.content)
        if data['success']:
            cookie = response.headers.get('Set-Cookie')
            token = data['data']['synotoken']
            headers = {
                'Cookie': cookie,
                'X-SYNO-TOKEN': token,
            }
        else:
            logger.error(response.content)
    except Exception as e:
        logger.error(e)


def get_tags():
    url = f'{base_url}/webapi/entry.cgi/{api_pre}.Browse.GeneralTag'
    data = {
        'api': f'{api_pre}.Browse.GeneralTag',
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
    else:
        if data['error']['code'] in token_error_code:
            get_token()
        logger.info(response.content)
    return []


def get_time_line():
    url = f'{base_url}/webapi/entry.cgi/{api_pre}.Browse.Timeline'
    data = {
        'api': f'{api_pre}.Browse.Timeline',
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
        list = get_photos()
        has_more = list is not None and len(list) > 0
        if not has_more:
            break
        detect_photo_list(list)
        offset += limit
        logger.info(f'识别到猫 %d 张图片, 共识别 %d 张图片', len(detect_list), len(done_list))


def detect_photo_list(list):
    for i, p in enumerate(tqdm(list)):
        logger.debug(f"{i + 1}/{len(list)}")
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
            detect_list.append(p)
    add_to_done_list(list)


def get_photos():
    logger.info(f'current offset = {offset} limit = {limit}')
    url = f'{base_url}/webapi/entry.cgi/{api_pre}.Browse.Item'
    data = {
        "api": f"{api_pre}.Browse.Item",
        "method": "list",
        "version": "1",
        "offset": offset,
        "limit": limit,
        "additional": '["thumbnail"]',
        "timeline_group_unit": '"day"',
        #     'start_time':,
        # 'end_time':
    }
    # logger.info(headers)
    response = requests.post(url, data=data, headers=headers)
    data = json.loads(response.content)
    # logger.info(data)
    if data['success']:
        list = data['data']['list']
        logger.info(f'get_photos: {len(list)}')
        return list
    else:
        if data['error']['code'] in token_error_code:
            get_token()
        logger.error(response.content)
        return None


def detect_image(image_content):
    is_cat = detect(image_content)
    if is_cat:
        return True
    else:
        return False


def get_photo_by_id(id, cache_key, headers):
    # logger.info(f'{id}  {cache_key}')
    url = f'{base_url}/webapi/entry.cgi?id={id}&cache_key={cache_key}&type=unit&size=sm&api={api_pre}.Thumbnail&method=get&version=2&SynoToken=NXibb.RkEVsCY'
    # logger.info(url)
    headers[
        'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    headers['Accept-Encoding'] = 'gzip, deflate'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        logger.info(response.content)
    return False


def create_tag(tag_name):
    url = f'{base_url}/webapi/entry.cgi/{api_pre}.Browse.GeneralTag'
    data = {
        'api': f'{api_pre}.Browse.GeneralTag',
        'method': 'create',
        'version': '1',
        'name': tag_name,
    }
    response = requests.post(url, data, headers=headers)
    data = json.loads(response.content)
    if data['success']:
        logger.info('标签添加成功')
        tags.append(data['data']['tag'])
    else:
        if data['error']['code'] in token_error_code:
            get_token()
        logger.info('标签添加失败')


def bind_tag(id, tag_name):
    tag_id = get_tag_id_by_name(tag_name)

    if tag_id is None:
        create_tag(tag_name)
        tag_id = get_tag_id_by_name(tag_name)

    url = f'{base_url}/webapi/entry.cgi/{api_pre}.Browse.Item'
    data = {
        'api': f'{api_pre}.Browse.Item',
        'method': 'add_tag',
        'version': '1',
        'id': f'[{id}]',
        'tag': f'[{tag_id}]'
    }
    # logger.info(data)
    response = requests.post(url, data, headers=headers)
    data = json.loads(response.content)
    if data['success']:
        logger.info('绑定标签成功')
        return True
    else:
        if data['error']['code'] in token_error_code:
            get_token()
        logger.info('添加标签失败')
        return False


def get_tag_id_by_name(tag_name):
    for tag in tags:
        if tag['name'] == tag_name:
            return tag['id']
    return None


def read_done_list():
    try:
        logger.info('读取已完成列表')
        done_list_file = get_done_list_file_path()
        with open(done_list_file, 'r') as f:
            data = json.load(f)
        global done_list
        done_list = data
    except FileNotFoundError:
        os.mknod(done_list_file)
        logger.info("文件创建成功！")
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


def init_var():
    global mode
    global api_pre
    global username
    global pwd
    global base_url
    username = os.environ['user']
    pwd = os.environ['pwd']
    mode = os.environ.get('mode', 'person')
    ip = os.environ.get('ip', '127.0.0.1:5000')
    if mode == 'person':
        api_pre = 'SYNO.Foto'
    else:
        api_pre = 'SYNO.FotoTeam'
    base_url = f'http://{ip}'


def start():
    init_var()
    read_done_list()
    get_token()
    global tags
    tags = get_tags()
    logger.info(tags)
    start_indexing()


if __name__ == '__main__':
    log.init_log()
    init_var()
    start_indexing()
