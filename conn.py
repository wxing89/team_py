#!/usr/bin/python2.7
# -*- coding:utf8 -*-

cnf = 'db.ini'

mydb = {}

f = open(cnf)
for line in f:
    try:
        x, y = line.split('=')
        mydb[x.strip()] = y.strip()
    except ValueError:
        pass

f.close()


import MySQLdb
import order

try:
    conn=MySQLdb.connect(host=mydb['host'], port=int(mydb['port']), 
        user=mydb['user'],passwd=mydb['passwd'],db=mydb['dbname'])
    
except MySQLdb.Error, e:
    print 'Mysql Error %d: %s' % (e.args[0], e.args[1])




