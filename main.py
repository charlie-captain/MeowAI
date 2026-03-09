import sys
import os

from src.executor import executor
from src.api import server
from src.config import config
from src.detect import detect
from src.log import logger

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            os.environ[key.strip()] = value.strip().rstrip('/')
    config.init_config()
    logger.init_log()
    detect.init_model()
    executor = executor.init_executor()
    server.start(executor)
    executor.stop()
