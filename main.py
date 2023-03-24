import time

from src.api import api
from src.detect import detect
from src.log import logger
from src.config import config

if __name__ == '__main__':
    logger.init_log()
    config.init_config()
    detect.init_model()
    api.start()
