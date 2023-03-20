import os
import re
import shutil
import time

import torch
from PIL import Image

model = None


def init_model():
    global model
    start_time = time.time()
    print('加载模型...')
    model = torch.hub.load('./yolov5', 'custom', source='local', path='./yolov5s.pt')
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    print(f"加载模型：{elapsed_time} 秒")


def detect(image_path):
    start_time = time.time()
    try:
        image = Image.open(image_path)
        image = image.resize((640, 640))
        results = model(image)
        # 获取检测框、置信度和类别标签
        scores = results.xyxy[0][:, 4].numpy()
        labels = results.xyxy[0][:, 5].numpy()

        lable_index = labels[0]
        label_text = model.names[lable_index]
        print(label_text)
        print(scores)
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        print(f"方法执行时间为：{elapsed_time} 秒")

        if label_text == 'cat':
            print('识别为猫')
            return True
        else:
            return False
    except:
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


if __name__ == '__main__':
    init_model()
    base = './data'
    file_list = get_filelist(base)
    for file in file_list:
        print(file)
        is_cat = detect(file)
        if is_cat:
            file_name = os.path.basename(file)
            new_file_path = './results/' + file_name
            shutil.copy2(file, new_file_path)
