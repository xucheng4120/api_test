# utils/data_loader.py
# 读取 yaml 数据的工具类

import yaml
import os

def load_yaml(filename):
    """读取 data 目录下的 yaml 文件"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", filename)
    
    with open(file_path, encoding="utf-8") as f:
        return yaml.safe_load(f)