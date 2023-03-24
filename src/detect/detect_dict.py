from src.config import config

classes_dict = {
    "person": "人类",
    "bicycle": "自行车",
    "car": "汽车",
    "motorcycle": "摩托车",
    "airplane": "飞机",
    "bus": "公交车",
    "train": "火车",
    "truck": "卡车",
    "boat": "船",
    "traffic light": "红绿灯",
    "fire hydrant": "消防栓",
    "stop sign": "停车标志",
    "parking meter": "停车场标线",
    "bench": "长凳",
    "bird": "鸟",
    "cat": "猫",
    "dog": "狗",
    "horse": "马",
    "sheep": "羊",
    "cow": "牛",
    "elephant": "大象",
    "bear": "熊",
    "zebra": "斑马",
    "giraffe": "长颈鹿",
    "clothing": "衣服",
    "handbag": "手提包",
    "backpack": "背包",
    "hat": "帽子",
    "shoe": "鞋子",
    "eye glasses": "眼镜",
    "watch": "手表",
    "cup": "杯子",
    "plate": "餐具",
    "chair": "椅子",
    "table": "餐桌",
    "tv": "立式电视",
    "computer": "电脑",
    "cell phone": "手机",
    "microwave": "微波炉",
    "oven": "烤箱",
    "toaster": "烤面包机",
    "sink": "水槽",
    "refrigerator": "冰箱",
    "bottle": "瓶子",
    "book": "书",
    "clock": "时钟",
    "plant": "植物",
    "sofa": "沙发",
    "potted plant": "盆栽",
    "bed": "床",
    "mirror": "镜子",
    "dining table": "餐厅桌子",
    "curtain": "窗帘",
    "bathtub": "浴缸",
    "shower": "淋浴器",
    "toilet": "厕所",
    "tv remote": "电视遥控器",
    "keyboard": "键盘",
    "guitar": "吉他",
    "drum": "打击乐器",
    "speaker": "音箱",
    "vacuum": "吸尘器",
    "scissors": "剪刀",
    "lion": "狮子",
    "tiger": "虎",
    "panda": "熊猫",
    "snake": "蛇",
    "bee": "蜜蜂"
}

# 是否标签全部, 根据上面detect_class判断
is_detect_all = False


def init_model_var():
    global is_detect_all
    detect_class = config.detect_class
    for c in detect_class:
        if c == 'all':
            is_detect_all = True


def has_label(label):
    if is_detect_all:
        return is_label_in_dict(label)
    else:
        for d in config.detect_class:
            if d == label:
                return is_label_in_dict(d)


def is_label_in_dict(key):
    return key in classes_dict


def get_tag_by_label(label):
    return classes_dict[label]
