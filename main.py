from src.api import server
from src.config import config
from src.detect import detect
from src.log import logger

if __name__ == '__main__':
    config.init_config()
    logger.init_log()
    detect.init_model()
    server.start()
