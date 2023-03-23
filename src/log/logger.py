import logging
import sys

logger = logging.getLogger('meow')


def init_log():
    # 设置Logger对象的日志级别
    logger.setLevel(logging.INFO)

    # 创建一个StreamHandler对象，指定输出到sys.stdout
    stream_handler = logging.StreamHandler(sys.stdout)

    # 设置StreamHandler对象的日志级别
    stream_handler.setLevel(logging.INFO)

    # 创建一个FileHandler对象，指定输出到log.txt文件
    file_handler = logging.FileHandler('logs.txt')

    # 设置FileHandler对象的日志级别
    file_handler.setLevel(logging.INFO)

    # 创建一个Formatter对象，指定日志格式
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

    # 为两个Handler对象设置Formatter对象
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
