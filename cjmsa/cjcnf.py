#!/usr/bin/env python
# -*- coding:utf8 -*-

import configparser
import sys

from cjlog import CJLog


class CJCnf():
    cnf = configparser.ConfigParser()
    file_cnf = {}
    mssql_cnf = {}
    def __init__(self, filename='default.ini'):
        self.filename = filename
        self.read_cnf()
        self.init_cnf()

    def read_cnf(self):
        CJLog.info("read configure file {0:s}".format(self.filename))
        try:
            with open(self.filename) as f:
                self.cnf.read_file(f)
        except Exception, e:
            CJLog.error('read configure file failed.')
            CJLog.error(str(e))
            sys.exit(128)

    def init_cnf(self):
        self.init_file()
        self.init_mssql()

    def init_file(self):
        self.cnf['file'].setdefault('directory', 'data')
        self.cnf['file'].setdefault('filename', 'example.dat')

        self.file_cnf['directory'] = self.cnf.get('file', 'directory', fallback='data')
        self.file_cnf['filename']  = self.cnf.get('file', 'filename',  fallback='example.dat')

    def init_mssql(self):
        self.cnf['mssql'].setdefault('host', 'localhost')
        self.cnf['mssql'].setdefault('port', '3306')
        self.cnf['mssql'].setdefault('user', '')
        self.cnf['mssql'].setdefault('passwd', '')
        self.cnf['mssql'].setdefault('db', '')
        self.cnf['mssql'].setdefault('character_set', 'utf8')

        self.mssql_cnf['host']    = self.cnf.get('mssql', 'host',    fallback='localhost')
        self.mssql_cnf['port']    = self.cnf.get('mssql', 'port',    fallback='1433')
        self.mssql_cnf['user']    = self.cnf.get('mssql', 'user',    fallback='')
        self.mssql_cnf['passwd']  = self.cnf.get('mssql', 'passwd',  fallback='')
        self.mssql_cnf['db']      = self.cnf.get('mssql', 'db',      fallback='')
        self.mssql_cnf['charset'] = self.cnf.get('mssql', 'charset', fallback='utf8')

    def write_cnf(self, filename='default.ini'):
        CJLog.info("write config info to {0:s}".format(filename))
        with open(filename, 'w') as f:
            self.cnf.write(f)
