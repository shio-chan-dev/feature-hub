import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from logging.handlers import TimedRotatingFileHandler
from config import LOG_DIR

# 创建目录
LOG_DIR.mkdir(parents=True, exist_ok=True)

def setup_logger(name=__name__):
    """
    创建并配置日志记录器，每天生成新的日志文件
    
    Args:
        name (str): 记录器名称（通常使用 __name__）
    
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 创建记录器
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 捕获所有级别日志
    
    # 如果记录器已有处理器，直接返回（避免重复添加）
    if logger.hasHandlers():
        return logger
    
    # 日志格式
    formatter = logging.Formatter(
        "%(asctime)s | %(name)-24s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 文件处理器 - 按天轮转（记录所有DEBUG及以上级别）
    debug_file_handler = TimedRotatingFileHandler(
        filename=LOG_DIR / "app_debug.log",
        when="midnight",  # 每天午夜轮转
        interval=1,       # 每天一次
        encoding="utf-8"
    )
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    debug_file_handler.suffix = "%Y-%m-%d"  # 日志文件后缀格式
    
    # 重要日志文件 - 按天轮转（只记录INFO及以上级别）
    info_file_handler = TimedRotatingFileHandler(
        filename=LOG_DIR / "app_info.log",
        when="midnight",  # 每天午夜轮转
        interval=1,       # 每天一次
        encoding="utf-8"
    )
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(formatter)
    info_file_handler.suffix = "%Y-%m-%d"  # 日志文件后缀格式
    
    # 控制台处理器（只显示INFO及以上级别）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # 添加处理器到记录器
    logger.addHandler(debug_file_handler)
    logger.addHandler(info_file_handler)
    logger.addHandler(console_handler)
    
    return logger

# 创建全局默认记录器
logger = setup_logger("main")
