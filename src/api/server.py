import json
import os
import time
from typing import Optional

from src import log
from src.api import api
from src.detect import detect, detect_dict
from src.executor import executor
from src.locale import locale
from src.log.logger import logger

score_threshold = 0.7
offset = 0
limit = 100
# 识别成功列表
detect_list = []
done_list = []
_ = locale.lc
_executor: Optional[executor.DetectExecutor] = None


class DetectFile:

    def __init__(self, id, filename, type, tag, model, score, exclude, cost):
        self.id = id
        self.filename = filename
        self.type = type
        self.tag = tag
        self.model = model
        self.score = score
        self.exclude = exclude
        self.cost = cost


class DetectFileEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DetectFile):
            return {'id': obj.id,
                    'filename': obj.filename,
                    'type': obj.type,
                    'tag': obj.tag,
                    'model': obj.model,
                    'score': obj.score,
                    'exclude': obj.exclude,
                    'cost': obj.cost
                    }
        return json.JSONEncoder.default(self, obj)


class DetectFileDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kwargs)

    def dict_to_object(self, d):
        if 'id' in d:
            return DetectFile(d['id'], d['filename'], d['type'], d['tag'], d['model'], d['score'], d.get('exclude'),
                              d.get('cost'))
        return d


def start_indexing():
    global offset
    global detect_list
    has_more = True
    while True:
        while has_more:
            list = api.get_photos(offset, limit)
            has_more = list is not None and len(list) > 0
            if not has_more:
                break
            detect_photo_list(list)
            offset += limit
            text_info = _("Detect %d images, total handle %d photos")
            logger.info(f'{text_info}', len(detect_list), len(done_list))
            detect_list = []
        text_sleep = _("Sleep...")
        logger.info(text_sleep)
        # sleep for a while
        time.sleep(60 * 5)
        # check has more
        total = api.count_total_photos()
        if total > len(done_list):
            has_more = True
            text_wake = _("Wake...")
            logger.info(text_wake)
            # reset offset
            offset = 0


def detect_photo(id, p):
    start_time = time.time()
    thumbnail = p['additional']['thumbnail']
    cache_key = thumbnail['cache_key']
    image_content = api.get_photo_by_id(id, cache_key, api.headers)
    label_text, score = detect.detect(image_content)
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    if detect_dict.is_label_in_dict(label_text):
        detect_tag = detect_dict.get_tag_by_label(label_text, locale.language)
    else:
        detect_tag = None
    score = round(score, 3) if score else 0
    is_exclude = detect_dict.is_label_exclude(label_text)
    detect_file = DetectFile(id, filename=p['filename'], type=p['type'], tag=detect_tag, model=detect.model_name,
                             score=score, exclude=is_exclude, cost=elapsed_time)
    if detect_tag is not None and score >= score_threshold and not is_exclude:
        exist_tags = p['additional']['tag']
        bind_tag(id, tag_name=detect_tag, exist_tags=exist_tags)
    return detect_file


def detect_photo_list(list):
    global detect_list
    start_time = time.time()
    for i, p in enumerate(list):
        id = p['id']
        if has_done(id):
            continue
        _executor.add_task(executor.DetectTask(i, id, len(list), p, detect_photo))
    _executor.run()
    results: Optional[map] = _executor.wait_completion()
    done_list = []
    for key, value in results.items():
        if value.tag is not None:
            detect_list.append(value)
        done_list.append(value)
    end_time = time.time()
    logger.debug(f'detect_photo_list cost = {end_time - start_time}s')
    add_to_done_list(done_list)


def read_done_list():
    try:
        done_list_file = get_done_list_file_path()
        with open(done_list_file, 'r') as f:
            data = json.load(f, cls=DetectFileDecoder)
        global done_list
        done_list = data
        text_done = _("read done_list: ")
        logger.info(f'{text_done}{len(done_list)}')
    except FileNotFoundError:
        os.mknod(done_list_file)
        logger.info(_("done_list created！"))
    except Exception as e:
        logger.exception(e)


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
        json.dump(done_list, f, cls=DetectFileEncoder, ensure_ascii=False)


def bind_tag(id, tag_name, exist_tags):
    tag_id = api.get_tag_id_by_name(tag_name)

    if tag_id is None:
        api.create_tag(tag_name)
        tag_id = api.get_tag_id_by_name(tag_name)

    if exist_tags and len(exist_tags) > 0:
        for e_tag in exist_tags:
            e_tag_name = e_tag['name']
            if e_tag_name == tag_name:
                return

    api.bind_tag(id, tag_id, tag_name)


def start(executor):
    global _executor
    _executor = executor
    api.init_var()
    read_done_list()
    start_indexing()


if __name__ == '__main__':
    log.init_log()
    api.init_var()
    start_indexing()
