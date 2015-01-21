#!/usr/bin/env python
# -*- coding:utf8 -*-

import logging
import logging.handlers

class CJLog():
    logger = logging.getLogger()
    def __init__(self, filename='default.log'):
        self.logfile = filename
        self.logger.setLevel(level=logging.DEBUG)
        self.logger.addHandler(self.console_log())
        self.logger.addHandler(self.file_log())

    def console_log(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level=logging.DEBUG)
        console_formatter = logging.Formatter(fmt='[%(filename)s - %(levelname)s] %(message)s')
        console_handler.setFormatter(fmt=console_formatter)
        return console_handler

    def file_log(self):
        file_handler = logging.handlers.RotatingFileHandler(filename=self.logfile,
                                                            mode='a',
                                                            maxBytes=10*1024,
                                                            backupCount=100)
        file_handler.setLevel(level=logging.INFO)
        file_formatter = logging.Formatter(fmt='[%(asctime)s - %(filename)s - %(levelname)s] %(message)s',
                                           datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(fmt=file_formatter)
        return file_handler

    @classmethod
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    @classmethod
    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    @classmethod
    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    @classmethod
    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    @classmethod
    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)
