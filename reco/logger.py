#!/usr/bin/env python
# -*- coding:utf8 -*-

import logging


# define logger
logger = logging.getLogger(name='logger')
logger.setLevel(level=logging.DEBUG)

# console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(level=logging.DEBUG)
console_formatter = logging.Formatter(fmt='[%(filename)s - %(levelname)s] %(message)s')
console_handler.setFormatter(fmt=console_formatter)

# file handler
file_handler = logging.FileHandler(filename='tuna.log', mode='a')
file_handler.setLevel(level=logging.INFO)
file_formatter = logging.Formatter(fmt='[%(asctime)s - %(filename)s - %(levelname)s] %(message)s',
                                   datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(fmt=file_formatter)

# add handler to logger
logger.addHandler(hdlr=console_handler)
logger.addHandler(hdlr=file_handler)


def test():
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')
