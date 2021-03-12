# -*- coding: utf-8 -*-
import os
import sys
import time
import logging
import inspect
from logging.handlers import RotatingFileHandler


dir = "C:\\Users\\Administrator\\AppData\\Local\\lsTool"

if not os.path.isdir(dir):
    os.makedirs(dir)
handlers = {logging.INFO: os.path.join(dir, 'info.log'),

            logging.ERROR: os.path.join(dir, 'error.log')
            }


def createHandlers():
    logLevels = handlers.keys()

    for level in logLevels:
        path = os.path.abspath(handlers[level])
        handlers[level] = RotatingFileHandler(path, maxBytes=10000, backupCount=2, encoding='utf-8')

# 加载模块时创建全局变量

createHandlers()


class PyLog(object):

    def printfNow(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def __init__(self):
        self.__loggers = {}

        logLevels = handlers.keys()

        for level in logLevels:
            logger = logging.getLogger(str(level))

            logger.addHandler(handlers[level])

            logger.setLevel(level)

            self.__loggers.update({level: logger})

    def getLogMessage(self, level, message):
        frame, filename, lineNo, functionName, code, unknowField = inspect.stack()[2]

        '''日志格式：[时间] [类型] [记录代码] 信息'''

        return "[%s] [%s] %s" % (self.printfNow(), level, message)

    def info(self, message):
        message = self.getLogMessage("info", message)

        self.__loggers[logging.INFO].info(message)

    def error(self, message):
        message = self.getLogMessage("error", message)

        self.__loggers[logging.ERROR].error(message)