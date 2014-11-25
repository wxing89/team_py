#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import pickle
import MySQLdb

import mycnf
from mycnf import cnf

from order import Order
from cf import CF


def read_file(order, filename='order201408'):
    print 'Read user-item data from file', filename, '...'
    f = open(filename)
    for line in f:
        temp = line.split('|')
        user, item = temp[0].strip(), temp[1].strip()
        order.addOrder(user, item)

def write_file(cf):
    print 'Write user-sim data into file ...'
    with open(os.path.join(cnf['dir'], 'user_sim.dat'), 'w') as f:
        for user in cf.user_sim:
            for u, sim in cf.user_sim[user]:
                f.write('|'.join([user, u, str(sim), '\n']))

    print 'Write item-sim data into file ...'
    with open(os.path.join(cnf['dir'], 'item_sim.dat'), 'w') as f:
        for item in cf.item_sim:
            for i, sim in cf.item_sim[item]:
                f.write('|'.join([item, i, str(sim), '\n']))

def read_mysql(order):
    print 'Read user-item data from mysql ...'
    try:
        conn=MySQLdb.connect(host=cnf['host'], port=int(cnf['port']), 
            user=cnf['user'],passwd=cnf['passwd'],db=cnf['dbname'])
    except MySQLdb.Error, e:
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])

    sql = "SELECT * FROM sam_user_item"
    try:
        cur = conn.cursor()
        cur.execute(sql)

        results = cur.fetchall()
        for row in results:
            user = row[1]
            item = row[2]
            order.addOrder(user, item)
    except MySQLdb.Error, e:
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
    conn.close()

def write_mysql(cf):
    write_file(cf)
    try:
        conn=MySQLdb.connect(host=cnf['host'], port=int(cnf['port']), 
            user=cnf['user'],passwd=cnf['passwd'],db=cnf['dbname'])
    except MySQLdb.Error, e:
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])

    sql1 = "LOAD DATA LOCAL INFILE '%s' \
            REPLACE INTO TABLE sim_user \
            FIELDS TERMINATED BY '|' \
            LINES TERMINATED BY '\\n'" % (os.path.join(cnf['dir'], 'user_sim.dat'))
    sql2 = "LOAD DATA LOCAL INFILE '%s' \
            REPLACE INTO TABLE sim_item \
            FIELDS TERMINATED BY '|' \
            LINES TERMINATED BY '\\n'" % (os.path.join(cnf['dir'], 'item_sim.dat'))
    try:
        cur = conn.cursor()
        print 'Write user-sim data into mysql ...'
        print '[EXECUTE]', sql1
        cur.execute(sql1)
        print 'Write item-sim data into mysql ...'
        print '[EXECUTE]', sql1
        cur.execute(sql2)
    except MySQLdb.Error, e:            
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
        conn.rollback()
    conn.commit()

read_dict  = {'file' : read_file,
              'mysql': read_mysql}

write_dict = {'file' : write_file, 
              'mysql': write_mysql}

def main():
    mycnf.readCnf()
    readOrder = read_dict[cnf['source']]

    order = Order()
    readOrder(order)

    cf = CF(order)
    print 'Calculate user similarity ...'
    cf.userBased()
    print 'Calculate item similarity ...'
    cf.itemBased()

    writeSim = write_dict[cnf['source']]
    writeSim(cf)


if __name__ == '__main__':
    main()
