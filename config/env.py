"""
配置加载模块
负责读取 config.yaml 文件，并对外提供 config 字典
"""

import yaml   # 用于解析 YAML 文件
import os     # 用于处理文件路径

def load_config():
    """
    加载 config.yaml 配置文件
    返回一个字典，包含 base_url、user 等配置项
    """
    # 获取当前文件所在目录（即 config/ 文件夹）
    current_dir = os.path.dirname(__file__)
    # 拼接出 config.yaml 的完整路径
    config_path = os.path.join(current_dir, 'config.yaml')

    # 以只读方式打开，编码为 UTF-8
    with open(config_path, 'r', encoding='utf-8') as f:
        # yaml.safe_load() 把 YAML 文本解析成 Python 字典
        return yaml.safe_load(f)

# 在模块被导入时，立即执行一次 load_config()
# 这样其他地方直接 from config.env import config 就能拿到配置
config = load_config()