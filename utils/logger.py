# utils/logger.py
# 获取日志器，同时输出到控制台和文件
# 日志文件按日期命名，方便管理和查找，日志格式包含时间、日志级别和消息内容，日志级别设置为 DEBUG，方便调试和问题定位，避免重复添加 handler 导致日志重复输出
# 使用 logging 模块实现日志功能，日志文件保存在 logs 目录下，自动创建目录和文件，支持中文日志内容，编码设置为 utf-8
# -*- coding: utf-8 -*-

import logging
import os
from datetime import datetime

def get_logger(name="api_test"):
    """获取日志器，同时输出到控制台和文件"""

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # 避免重复添加 handler

    logger.setLevel(logging.DEBUG)

    # 日志格式
    fmt = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(fmt)

    # 文件输出，按日期命名
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger