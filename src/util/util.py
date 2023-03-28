from src.detect import detect_dict
from src.log import logger
from src.api import api
from src.config import config


# 移除全部已经识别的标签, 谨慎使用
# Warning: remove all recognize tags, use carefully
def remove_all_exist_tags():
    offset = 0
    limit = 100
    has_more = True
    while (has_more):
        list = api.get_photos(offset, limit)
        has_more = list is not None and len(list) > 0
        if not has_more:
            break
        for p in list:
            tags = p['additional']['tag']
            tag_ids = []
            for tag in tags:
                tag_name = tag['name']
                if tag_name in detect_dict.classes_dict.values():
                    tag_ids.append(tag['id'])
            if len(tag_ids) > 0:
                api.remove_tags(p['id'], tag_ids)
        offset += limit


if __name__ == '__main__':
    config.init_config()
    logger.init_log()
    api.init_var()
    remove_all_exist_tags()
