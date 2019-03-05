import os
import logging


def getFileLogger(logDir, fileName):
    logger = logging.getLogger('MyFileLogger')
    # file_handler for our logger
    if not os.path.exists(logDir):
        os.mkdir(logDir)
    logPath = os.path.join(logDir, fileName)
    file_handler = logging.FileHandler(logPath)
    formatter = logging.Formatter('%(asctime)s | %(filename)s:%(lineno)s - %(funcName)-12s | %(levelname)-10s | %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
