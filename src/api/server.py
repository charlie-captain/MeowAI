import json
import os
import time

from src import log
from src.api import api
from src.detect import detect, detect_dict
from src.log.logger import logger

offset = 0
limit = 100
# 识别成功列表
detect_list = []
done_list = []


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
            return {'id': obj.id,
                    'filename': obj.filename,
                    'type': obj.type,
                    'tag': obj.tag,
                    'model': obj.model}
        return json.JSONEncoder.default(self, obj)


class DetectFileDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kwargs)

    def dict_to_object(self, d):
        if 'id' in d:
            return DetectFile(d['id'], d['filename'], d['type'], d['tag'], d['model'])
        return d


def start_indexing():
    global offset
    global detect_list
    has_more = True
    while (has_more):
        list = api.get_photos(offset, limit)
        has_more = list is not None and len(list) > 0
        if not has_more:
            break
        detect_photo_list(list)
        offset += limit
        logger.info(f'成功识别到 %d 张图片, 共处理 %d 张图片', len(detect_list), len(done_list))
        detect_list = []


def detect_photo_list(list):
    global detect_list
    done_list = []
    for i, p in enumerate(list):
        id = p['id']
        if has_done(id):
            continue
        start_time = time.time()
        thumbnail = p['additional']['thumbnail']
        cache_key = thumbnail['cache_key']
        image_content = api.get_photo_by_id(id, cache_key, api.headers)
        detect_tag = detect.detect(image_content)
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        logger.info(f'进度: {i + 1}/{len(list)}, {p["filename"]} 识别为 {detect_tag}, 耗时为 {elapsed_time} 秒')
        logger.debug(f'{id} {cache_key} {detect_tag}')
        detect_file = DetectFile(id, filename=p['filename'], type=p['type'], tag=None, model=detect.model_name)
        if detect_tag is not None:
            exist_tags = p['additional']['tag']
            bind_tag(id, tag_name=detect_tag, exist_tags=exist_tags)
            detect_file.tag = detect_tag
            detect_list.append(p)
        done_list.append(detect_file)
    add_to_done_list(done_list)


def read_done_list():
    try:
        done_list_file = get_done_list_file_path()
        with open(done_list_file, 'r') as f:
            data = json.load(f, cls=DetectFileDecoder)
        global done_list
        done_list = data
        logger.info(f'读取已完成列表: {len(done_list)}')
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
        if d.id == id and d.model == detect.model_name and (
                d.tag is not None or (d.tag is None and d.model == detect.model_name)):
            return True
    return False


def add_to_done_list(list):
    if len(list) == 0:
        return
    for done in list:
        done_list.append(done)
    with open(get_done_list_file_path(), 'w') as f:
        json.dump(done_list, f, cls=DetectFileEncoder)


def bind_tag(id, tag_name, exist_tags):
    tag_id = api.get_tag_id_by_name(tag_name)

    if tag_id is None:
        api.create_tag(tag_name)
        tag_id = api.get_tag_id_by_name(tag_name)

    if exist_tags and len(exist_tags) > 0:
        for e_tag in exist_tags:
            e_tag_name = e_tag['name']
            if e_tag_name != tag_name:
                if e_tag_name in detect_dict.classes_dict.values():
                    # todo remove old tag
                    break

    api.bind_tag(id, tag_id, tag_name)


def start():
    api.init_var()
    read_done_list()
    start_indexing()


if __name__ == '__main__':
    log.init_log()
    api.init_var()
    start_indexing()
