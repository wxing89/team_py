#!/usr/bin/env python
# -*- coding:utf8 -*-

import configparser
import sys

from mylog import MyLog

cnf = configparser.ConfigParser()

default_cnf = {}
file_cnf = {}
mysql_cnf = {}
redis_cnf = {}

def read_cnf(cnf_file):
    try:
        with open(cnf_file) as f:
            cnf.read_file(f)
    except Exception, e:
        MyLog.logger.error('read configure file failed.')
        MyLog.logger.error(str(e))
        sys.exit(128)


def init_cnf(cnf_file='default.ini'):
    # read config
    read_cnf(cnf_file)
    # init default config
    init_default()
    # init file config
    init_file()
    # init mysql config
    init_mysql()
    # init redis config
    init_redis()


def init_default():
    cnf['default'].setdefault('source', 'file')
    cnf['default'].setdefault('target', 'mysql')

    default_cnf['source'] = cnf.get('default', 'source', fallback='file')
    default_cnf['target'] = cnf.get('default', 'target', fallback='mysql')


def init_file():
    cnf['file'].setdefault('directory', './data')
    cnf['file'].setdefault('filename', 'user_item.dat')

    file_cnf['directory'] = cnf.get('file', 'directory', fallback='./data')
    file_cnf['filename']  = cnf.get('file', 'filename', fallback='user_item.dat')



def init_mysql():
    cnf['mysql'].setdefault('host', 'localhost')
    cnf['mysql'].setdefault('port', '3306')
    cnf['mysql'].setdefault('user', '')
    cnf['mysql'].setdefault('passwd', '')
    cnf['mysql'].setdefault('db', '')
    cnf['mysql'].setdefault('character_set', 'utf8')

    mysql_cnf['host']    = cnf.get('mysql', 'host', fallback='localhost')
    mysql_cnf['port']    = cnf.getint('mysql', 'port', fallback=3306)
    mysql_cnf['user']    = cnf.get('mysql', 'user', fallback='')
    mysql_cnf['passwd']  = cnf.get('mysql', 'passwd', fallback='')
    mysql_cnf['db']      = cnf.get('mysql', 'db', fallback='')
    mysql_cnf['charset'] = cnf.get('mysql', 'character_set', fallback='utf8')


def init_redis():
    cnf['redis'].setdefault('host', '127.0.0.1')
    cnf['redis'].setdefault('port', '6379')
    cnf['redis'].setdefault('db', '0')

    redis_cnf['host'] = cnf.get('redis', 'host', fallback='localhost')
    redis_cnf['port'] = cnf.getint('redis', 'port', fallback=6379)
    redis_cnf['db']   = cnf.getint('redis', 'db', fallback=0)


def write_cnf(filename='default.ini'):
    with open(filename, 'w') as f:
        cnf.write(f)


def main():
    init_cnf()
    write_cnf()


if __name__ == "__main__":
    main()