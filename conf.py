#!/usr/bin/env python
# -*- coding:utf8 -*-

import configparser
import sys

cnf_file = 'init.cnf'

cnf = configparser.ConfigParser()

default_cnf = {}
file_cnf = {}
mysql_cnf = {}
redis_cnf = {}

def readcnf():
    try:
        cnf.read(cnf_file)
    except Exception, e:
        print "Read configure file failed."
        print e
        sys.exit(128)

def initcnf():
    # init default config
    init_default()
    # init file config
    init_file()
    # init mysql config
    init_mysql()
    # init redis config
    init_redis()


def init_default():
    default_cnf['source'] = cnf.get('default', 'source', fallback='file')
    default_cnf['target'] = cnf.get('default', 'target', fallback='mysql')


def init_file():
    file_cnf['directory'] = cnf.get('file', 'directory', fallback='./data')
    file_cnf['filename']  = cnf.get('file', 'filename', fallback='user_item.dat')


def init_mysql():
    mysql_cnf['host']    = cnf.get('mysql', 'host', fallback='localhost')
    mysql_cnf['port']    = cnf.getint('mysql', 'port', fallback=3306)
    mysql_cnf['user']    = cnf.get('mysql', 'user', fallback='')
    mysql_cnf['passwd']  = cnf.get('mysql', 'passwd', fallback='')
    mysql_cnf['db']      = cnf.get('mysql', 'db', fallback='')
    mysql_cnf['charset'] = cnf.get('mysql', 'character_set', fallback='utf8')


def init_redis():
    redis_cnf['host'] = cnf.get('redis', 'host', fallback='localhost')
    redis_cnf['port'] = cnf.getint('redis', 'port', fallback=6379)
    redis_cnf['db']   = cnf.getint('redis', 'db', fallback=0)


def writecnf(finename='default.ini'):
    with open(finename, 'w') as f:
        cnf.write(f)


def main():
    readcnf()
    initcnf()


if __name__ == "__main__":
    main()