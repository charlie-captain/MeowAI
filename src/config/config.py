import os

# 识别种类, 默认为猫咪, 如果为all则全部识别分类打tag
detect_class = ['cat']


def init_config():
    global detect_class
    detect_class = os.environ.get('detect_class', detect_class)

