import gettext

from src.config import config
from src.locale import locale
from src.log.logger import logger

_ = locale.lc
classes_dict = {"person": "人",
                "bicycle": "自行车",
                "car": "汽车",
                "motorcycle": "摩托车",
                "airplane": "飞机",
                "bus": "公共汽车",
                "train": "火车",
                "truck": "卡车",
                "boat": "船",
                "traffic light": "交通灯",
                "fire hydrant": "消防栓",
                "stop sign": "停止标志",
                "parking meter": "停车计时器",
                "bench": "长凳",
                "bird": "鸟",
                "cat": "猫",
                "dog": "狗",
                "horse": "马",
                "sheep": "绵羊",
                "cow": "奶牛",
                "elephant": "大象",
                "bear": "熊",
                "zebra": "斑马",
                "giraffe": "长颈鹿",
                "backpack": "背包",
                "umbrella": "雨伞",
                "handbag": "手提包",
                "tie": "领带",
                "suitcase": "手提箱",
                "frisbee": "飞盘",
                "skis": "滑雪板",
                "snowboard": "单板滑雪板",
                "sports ball": "运动球",
                "kite": "风筝",
                "baseball bat": "棒球棒",
                "baseball glove": "棒球手套",
                "skateboard": "滑板",
                "surfboard": "冲浪板",
                "tennis racket": "网球拍",
                "bottle": "瓶子",
                "wine glass": "酒杯",
                "cup": "杯子",
                "fork": "叉子",
                "knife": "刀",
                "spoon": "勺子",
                "bowl": "碗",
                "banana": "香蕉",
                "apple": "苹果",
                "sandwich": "三明治",
                "orange": "橙子",
                "broccoli": "西兰花",
                "carrot": "胡萝卜",
                "hot dog": "热狗",
                "pizza": "比萨饼",
                "donut": "甜甜圈",
                "cake": "蛋糕",
                "chair": "椅子",
                "couch": "沙发",
                "potted plant": "盆栽植物",
                "bed": "床",
                "dining table": "餐桌",
                "toilet": "厕所",
                "tv": "电视",
                "laptop": "笔记本电脑",
                "mouse": "鼠标",
                "remote": "遥控器",
                "keyboard": "键盘",
                "cell phone": "手机",
                "microwave": "微波炉",
                "oven": "烤箱",
                "toaster": "烤面包机",
                "sink": "水槽",
                "refrigerator": "冰箱",
                "book": "书",
                "clock": "时钟",
                "vase": "花瓶",
                "scissors": "剪刀",
                "teddy bear": "泰迪熊",
                "hair drier": "吹风机",
                "toothbrush": "牙刷"
                }

# 是否标签全部, 根据上面detect_class判断
is_detect_all = False


def init_model_var():
    global is_detect_all
    cur_config = config.curConfig
    logger.info(cur_config)
    exclude_class = cur_config.exclude_class
    is_detect_all = len(exclude_class) == 0
    text = _("exclude_class:")
    logger.info(f'{text} {exclude_class}')


def is_label_exclude(label):
    if is_detect_all:
        return False
    else:
        for d in config.curConfig.exclude_class:
            if d == label:
                return True
        return False


def is_label_in_dict(key):
    return key in classes_dict


def get_tag_by_label(label, language):
    if language == 'zh':
        return classes_dict[label]
    else:
        return label
