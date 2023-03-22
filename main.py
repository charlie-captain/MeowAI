import time

from src.api import api
from src.detect import detect
from src.log import logger

if __name__ == '__main__':
    logger.init_log()
    detect.init_model()
    api.start()
