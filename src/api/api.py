import json
import os
import time

import requests

from src.detect import detect_dict
from src.detect import detect
from src.log import logger as log
from src.log.logger import logger

base_url = 'http://127.0.0.1:5000'
cookie = None
token = None
headers = None
tags = []
offset = 0
limit = 100
done_list = []
# 识别文件夹
mode = 'person'
# api 前缀
api_pre = None
# 识别成功列表
detect_list = []
username = None
pwd = None
# token错误码
token_error_code = ['119', '120', '150']


class DetectFile:

    def __init__(self, id, filename, type, tag, model):
        self.id = id
        self.filename = filename
        self.type = type
        self.tag = tag
        self.model = model


class DetectFileEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DetectFile):
            return {"id": obj.id, "filename": obj.filename, "type": obj.type, "tag": obj.tag, "model": obj.model}
        return super().default(obj)


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
        logger.info(f'成功识别到 %d 张图片, 共处理 %d 张图片', len(detect_list), len(done_list))


def detect_photo_list(list):
    done_list = []
    for i, p in enumerate(list):
        id = p['id']
        if has_done(id):
            continue
        start_time = time.time()
        thumbnail = p['additional']['thumbnail']
        cache_key = thumbnail['cache_key']
        image_content = get_photo_by_id(id, cache_key, headers)
        detect_tag = detect.detect(image_content)
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        logger.info(f'进度: {i + 1}/{len(list)}, {p["filename"]} 识别为 {detect_tag}, 耗时为 {elapsed_time} 秒')
        logger.debug(f'{id} {cache_key} {detect_tag}')
        detect_file = DetectFile(id, filename=p['filename'], type=p['type'], tag=None, model=detect.model_name)
        if detect_tag is not None:
            bind_tag(id, tag_name=detect_tag)
            detect_file.tag = detect_tag
        done_list.append(detect_file)
    add_to_done_list(done_list)


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
        logger.info(f'标签创建成功: {tag_name}')
        tags.append(data['data']['tag'])
    else:
        if data['error']['code'] in token_error_code:
            get_token()
        logger.info(f'标签创建失败: {tag_name}')


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
    try:
        data = json.loads(response.content)
        if data['success']:
            logger.debug(f'标签绑定成功: id={id} {tag_name}')
            return True
        else:
            if data['error']['code'] in token_error_code:
                get_token()
            logger.error(f'标签绑定失败: id={id} {tag_name}')
            return False
    except Exception as e:
        logger.error(e)
        logger.error(f'标签绑定失败: id={id} {tag_name}')


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
            data = json.load(f, cls=DetectFileEncoder)
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
        if d.id == id and d.tag is not None:
            return True
    return False


def add_to_done_list(list):
    for done in list:
        done_list.append(done)
    with open(get_done_list_file_path(), 'w') as f:
        json.dump([obj.__dict__ for obj in done_list], f)


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
    detect_dict.init_model_var()


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
