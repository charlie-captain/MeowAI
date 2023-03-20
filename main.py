import time

import yolov5
from PIL import Image

model = None


def init_model():
    global model
    start_time = time.time()
    print('加载模型...')
    model = yolov5.load('yolov5s.pt')
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    print(f"加载模型：{elapsed_time} 秒")


def detect(image_path):
    start_time = time.time()
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


if __name__ == '__main__':
    init_model()
    image_path = './test-dog.jpg'
    detect(image_path)
    image_path = './test-meow.jpg'
    detect(image_path)
