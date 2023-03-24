import json
import os
import time
from io import BytesIO

import torch
from PIL import Image

from src.detect import detect_dict
from src.log.logger import logger


class DetectFile:

    def __init__(self, file_name, file_path):
        self.file_name = file_name
        self.file_path = file_path


model = None


def init_model():
    global model
    start_time = time.time()
    logger.info('加载模型...')
    try:
        model = torch.hub.load('./yolov5', 'custom', source='local', path='./yolov5s.pt')
    except Exception as e:
        logger.error(e)
        exit(-1)
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    logger.info(f"加载模型：{elapsed_time} 秒")


def detect(image_path):
    start_time = time.time()
    try:
        # logger.info(f"正在识别 %s", image_path)
        image = Image.open(BytesIO(image_path))
        image = image.resize((640, 640))
        results = model(image)
        # 获取检测框、置信度和类别标签
        scores = results.xyxy[0][:, 4].numpy()
        labels = results.xyxy[0][:, 5].numpy()
        if len(labels) == 0:
            # logger.info('没有识别到任何物体')
            return None
        label_index = labels[0]
        label_text = model.names[label_index]
        # logger.info(label_text)
        # print(scores)
        if detect_dict.has_label(label_text):
            logger.info(f'识别为 {label_text}')
            end_time = time.time()
            elapsed_time = round(end_time - start_time, 2)
            logger.info(f"方法执行时间为：{elapsed_time} 秒")
            return detect_dict.get_tag_by_label(label_text)
        else:
            return None
    except Exception as e:
        logger.exception("Error: %s", e)
        return None


def detect_dir():
    global files, f
    base = './data'
    detect_file_list = []
    for home, dirs, files in os.walk(base):
        for filename in files:
            # 判断是否是图片格式
            if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
                # 文件名列表，包含完整路径
                file = os.path.join(home, filename)
                # is_cat = detect(file)
                # if is_cat:
                #     file_name = os.path.basename(file)
                #     new_file_path = './results/' + file_name
                #     shutil.copy2(file, new_file_path)
                    # detect_file = DetectFile(file_name, file_path=file)
                    # detect_file_list.append(detect_file)
    json_str = json.dumps([f.__dict__ for f in detect_file_list])
    with open("./results/result.json", "w") as f:
        json.dump(json_str, f)
