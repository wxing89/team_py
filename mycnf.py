#!/usr/bin/env python
# -*- coding:utf8 -*-

import MySQLdb
import order

cnf_file = 'db.cnf'

cnf = {}

def readCnf():
    f = open(cnf_file)
    for line in f:
        try:
            x, y = line.split('=')
            cnf[x.strip()] = y.strip()
        except ValueError:
            pass
    f.close()

