import logging
import sys

from src.config import config

logger = logging.getLogger('meow')


def init_log():
    level = logging.INFO
    if config.is_debug:
        level = logging.DEBUG

    # 设置Logger对象的日志级别
    logger.setLevel(level)

    # 创建一个StreamHandler对象，指定输出到sys.stdout
    stream_handler = logging.StreamHandler(sys.stdout)

    # 设置StreamHandler对象的日志级别
    stream_handler.setLevel(level)

    # 创建一个FileHandler对象，指定输出到log.txt文件
    file_handler = logging.FileHandler('logs.txt')

    # 设置FileHandler对象的日志级别
    file_handler.setLevel(level)

    # 创建一个Formatter对象，指定日志格式
    format = '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    formatter = logging.Formatter(format, datefmt='%Y-%m-%d %H:%M:%S')

    # 为两个Handler对象设置Formatter对象
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
