import json
import logging
import os
import sys
import time
import torch
from PIL import Image

model = None
logger = logging.getLogger('meow')


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
        logger.info(f"正在识别 %s", image_path)
        image = Image.open(image_path)
        image = image.resize((640, 640))
        results = model(image)
        # 获取检测框、置信度和类别标签
        scores = results.xyxy[0][:, 4].numpy()
        labels = results.xyxy[0][:, 5].numpy()
        if len(labels) == 0:
            logger.info('没有识别到任何物体')
            return False
        lable_index = labels[0]
        label_text = model.names[lable_index]
        logger.info(label_text)
        # print(scores)
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        logger.info(f"方法执行时间为：{elapsed_time} 秒")

        if label_text == 'cat':
            logger.info('识别为猫')
            return True
        else:
            return False
    except Exception as e:
        logger.error("Error: %s", e)
        return False


def get_filelist(dir):
    Filelist = []
    for home, dirs, files in os.walk(dir):
        for filename in files:
            # 判断是否是图片格式
            if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
                # 文件名列表，包含完整路径
                Filelist.append(os.path.join(home, filename))
    return Filelist


class DetectFile:

    def __init__(self, file_name, file_path):
        self.file_name = file_name
        self.file_path = file_path


def init_log():
    # 设置Logger对象的日志级别
    logger.setLevel(logging.DEBUG)

    # 创建一个StreamHandler对象，指定输出到sys.stdout
    stream_handler = logging.StreamHandler(sys.stdout)

    # 设置StreamHandler对象的日志级别
    stream_handler.setLevel(logging.DEBUG)

    # 创建一个FileHandler对象，指定输出到log.txt文件
    file_handler = logging.FileHandler('logs.txt')

    # 设置FileHandler对象的日志级别
    file_handler.setLevel(logging.DEBUG)

    # 创建一个Formatter对象，指定日志格式
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

    # 为两个Handler对象设置Formatter对象
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)


if __name__ == '__main__':
    init_log()
    init_model()
    base = './data'
    detect_file_list = []
    for home, dirs, files in os.walk(base):
        for filename in files:
            # 判断是否是图片格式
            if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
                # 文件名列表，包含完整路径
                file = os.path.join(home, filename)
                is_cat = detect(file)
                if is_cat:
                    file_name = os.path.basename(file)
                    new_file_path = './results/' + file_name
                    # shutil.copy2(file, new_file_path)
                    detect_file = DetectFile(file_name, file_path=file)
                    detect_file_list.append(detect_file)

    json_str = json.dumps([f.__dict__ for f in detect_file_list])
    with open("./results/result.json", "w") as f:
        json.dump(json_str, f)
