#!/usr/bin/env python
# -*- coding:utf8 -*-

import configparser


config = configparser.ConfigParser()

config['default'] = {}
config['default']['source'] = 'mysql'
config['default']['target'] = 'mysql'

config['file'] = {
    'directory': './data',
    'filename': 'user_item.dat'
}

config['mysql'] = {
    'host': '192.168.9.36',
    'port': '3306',
    'user': 'tuna',
    'passwd': 'tuna',
    'db': 'userdb',
}

config['redis'] = {
    'host': '192.168.9.36',
    'port': '6379',
    'db': 0,
}


with open('default.ini', 'w') as configfile:
    config.write(configfile)


