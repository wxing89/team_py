#!/usr/bin/python2.7
# -*- coding:utf8 -*-


import MySQLdb

import conf
from conf import cnf

from order import Order
from sim import Sim

from cfrecommend import CFRecommend

def mysql_readorder(order, conn):
    """ 
    to be comment
    """
    try:
        cur = conn.cursor()
        sql = "SELECT user_id, item_id FROM sam_user_item"
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            order.addOrder(row[0], row[1])
    except MySQLdb.Error, e:
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
    finally:
        cur.close()

def mysql_readcf(cf, conn):
    """ 
    to be comment
    """
    try:
        cur = conn.cursor()
        sql = "SELECT user_1, user_2, sim FROM sim_user";
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            u1, u2, sim = row[0], row[1], row[2]
            cf.user_sim[u1] = cf.user_sim.get(u1, [])
            cf.user_sim[u1].append((u2, sim))

        sql = "SELECT item_1, item_2, sim FROM sim_item";
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            i1, i2, sim = row[0], row[1], row[2]
            cf.item_sim[i1] = cf.item_sim.get(i1, [])
            cf.item_sim[i1].append((i2, sim))
    except MySQLdb.Error, e:
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
    finally:
        cur.close()

def redis_readorder(order, conn):
    pass

def redis_readcf(cf, conn):
    pass

def getcf(cf, conn=None):
    pass

def getorder(cf, conn=None):
    pass

def getdata(order, cf):
    if mycnf.cnf['source'] != 'mysql':
        print 'Not implenmented'

    try:
        conn = MySQLdb.connect(host=cnf['mysql.host'],
                               port=int(cnf['mysql.port']),
                               user=cnf['mysql.user'],
                               passwd=cnf['mysql.passwd'],
                               db=cnf['mysql.db'],
                               connect_timeout=3,
                               local_infile=1)
        mysql_readorder(order, conn)
        mysql_readcf(cf, conn)
        conn.close()
    except MySQLdb.Error, e:
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])


def main():
    mycnf.readCnf()

    order = Order()
    cf = CF()
    getdata(order, cf)

    cfreco = CFRecommend(order=order, cf=cf)
    cfreco.cf_recommend()

    # write_cfreco_to_redis()

if __name__ == '__main__':
    main()
