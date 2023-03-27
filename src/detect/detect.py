import json
import os
import time
from io import BytesIO

import torch
from PIL import Image, ImageOps

from src.detect import detect_dict
from src.log.logger import logger

model = None
model_name = 'yolov5m6'


def init_model():
    global model
    global model_name
    start_time = time.time()
    model_name = os.environ.get('model', model_name)
    logger.info(f'加载模型: {model_name}')
    try:
        device = None
        if torch.cuda.is_available():
            logger.info("CUDA is available.")
            device = torch.device('cuda')
        else:
            logger.info("CUDA is not available.")

        if torch.backends.mps.is_available():
            logger.info("MPS is available.")
            device = torch.device("mps")
        else:
            logger.info("MPS is not available.")
        model_file = f'./{model_name}.pt'
        model = torch.hub.load('./yolov5', 'custom', source='local', path=model_file, device=device)
    except Exception as e:
        logger.error(e)
        exit(-1)
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    logger.info(f"加载模型：{elapsed_time} 秒")


def detect(image_path):
    try:
        # logger.info(f"正在识别 %s", image_path)
        image = Image.open(BytesIO(image_path))
        logger.debug(f'图片大小为: {image.width}x{image.height}')
        # 将图片调整为指定大小，并使用 padding 的方式进行调整
        new_size = (1280, 1280)
        image = ImageOps.pad(image, new_size)
        logger.debug(f'修改后图片大小为: {image.width}x{image.height}')
        results = model(image)
        # 将检测结果转换为 Dataframe
        df = results.pandas().xyxy[0]
        # 按照置信度得分从大到小排序
        df = df.sort_values(by='confidence', ascending=False)
        # 获取置信度最大的检测结果
        if len(df.values.tolist()) == 0:
            return None, None
        best_result = df.iloc[0]
        # 获取类别和置信度
        labels_index = best_result['class']
        confidence = best_result['confidence']
        if labels_index is None:
            # logger.info('没有识别到任何物体')
            return None, None
        label_text = model.names[labels_index]
        if detect_dict.has_label(label_text):
            return detect_dict.get_tag_by_label(label_text), confidence
        else:
            return None, None
    except Exception as e:
        logger.exception("Error: %s", e)
        return None, None


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
