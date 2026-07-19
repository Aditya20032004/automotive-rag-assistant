# src/logger.py
import logging
import os
import sys

# Ensure config paths are accessible
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def get_logger(name="automotive_rag"):
    """
    Initializes a dual console-and-file logging pipeline.
    Prevents duplicate handler attachments if called multiple times.
    """
    logger = logging.getLogger(name)
    
    # If logger is already configured, return it to prevent duplicate logs
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.INFO)
    
    # Production-grade log layout
    log_format = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)-8s [%(filename)s:%(lineno)d] : %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 1. Console stream handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    # 2. Permanent file handler in the project root folder
    log_file_path = os.path.join(config.ROOT_DIR, "automotive_rag.log")
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    
    return logger

# Single shared instance for the application
logger = get_logger()