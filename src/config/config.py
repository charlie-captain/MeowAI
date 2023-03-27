import json
import os

is_debug = False


class Config:
    # 排除种类
    exclude_class = []

    def __init__(self):
        super().__init__()
        config = self.read_local_config()
        if config and 'exclude_class' in config:
            self.exclude_class = config['exclude_class']

    def save_cur_config(self):
        with open(self.get_config_file_path(), 'w') as f:
            json.dump(self.__dict__, f)

    def get_config_file_path(self):
        root_path = os.path.abspath(os.getcwd())
        config_file = os.path.join(root_path, 'config')
        config_file = os.path.join(config_file, 'config.json')
        return config_file

    def read_local_config(self):
        try:
            with open(self.get_config_file_path(), 'r') as f:
                return json.load(f)
        except Exception as e:
            print(e)
        return None


curConfig = None


def init_config():
    global is_debug
    global curConfig
    is_debug = os.environ.get('debug', is_debug)
    print(f'当前环境: {"Debug环境" if is_debug else "正式环境"}')
    curConfig = Config()
    exclude_class = os.environ.get('exclude_class', None)
    if exclude_class:
        exclude_class = json.loads(exclude_class)
    if exclude_class and exclude_class != curConfig.exclude_class:
        curConfig.exclude_class = exclude_class
        curConfig.save_cur_config()

    print(f'当前配置为 {curConfig.__dict__}')
