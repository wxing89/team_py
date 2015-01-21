#!/usr/bin/env python
# -*- coding:utf8 -*-

import configparser
import sys

from mylog import MyLog


class MyCnf():
    cnf = configparser.ConfigParser()

    def __init__(self, filename='default.ini'):
        self.filename = filename
        self.file_cnf = {}
        self.mysql_cnf = {}
        self.redis_cnf = {}
        self.read_cnf()
        self.init_cnf()

    def read_cnf(self):
        MyLog.info("read configure file {0:s}".format(self.filename))
        try:
            with open(self.filename) as f:
                self.cnf.read_file(f)
        except Exception, e:
            MyLog.error('read configure file failed.')
            MyLog.error(str(e))
            sys.exit(128)

    def init_cnf(self):
        self.init_file()
        self.init_mysql()
        self.init_redis()

    def init_file(self):
        self.cnf['file'].setdefault('directory', './data')
        self.cnf['file'].setdefault('filename', 'example.dat')

        self.file_cnf['directory'] = self.cnf.get('file', 'directory', fallback='./data')
        self.file_cnf['filename'] = self.cnf.get('file', 'filename', fallback='example.dat')

    def init_mysql(self):
        self.cnf['mysql'].setdefault('host', 'localhost')
        self.cnf['mysql'].setdefault('port', '3306')
        self.cnf['mysql'].setdefault('user', '')
        self.cnf['mysql'].setdefault('passwd', '')
        self.cnf['mysql'].setdefault('db', '')
        self.cnf['mysql'].setdefault('character_set', 'utf8')

        self.mysql_cnf['host'] = self.cnf.get('mysql', 'host', fallback='localhost')
        self.mysql_cnf['port'] = self.cnf.getint('mysql', 'port', fallback=3306)
        self.mysql_cnf['user'] = self.cnf.get('mysql', 'user', fallback='')
        self.mysql_cnf['passwd'] = self.cnf.get('mysql', 'passwd', fallback='')
        self.mysql_cnf['db'] = self.cnf.get('mysql', 'db', fallback='')
        self.mysql_cnf['charset'] = self.cnf.get('mysql', 'character_set', fallback='utf8')

    def init_redis(self):
        self.cnf['redis'].setdefault('host', '127.0.0.1')
        self.cnf['redis'].setdefault('port', '6379')
        self.cnf['redis'].setdefault('db', '0')

        self.redis_cnf['host'] = self.cnf.get('redis', 'host', fallback='localhost')
        self.redis_cnf['port'] = self.cnf.getint('redis', 'port', fallback=6379)
        self.redis_cnf['db'] = self.cnf.getint('redis', 'db', fallback=0)

    def write_cnf(self, filename='default.ini'):
        MyLog.info("write config info to {0:s}".format(filename))
        with open(filename, 'w') as f:
            self.cnf.write(f)
