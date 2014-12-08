#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import sys
import pickle
import MySQLdb

import mycnf
from mycnf import cnf

from order import Order
from cf import CF

def cfUser(user, order, cf):
    _u_i = order.user_item
    sim_users = cf.user_sim[user]
    temp = {}

    for u, sim in sim_users:
        for item in _u_i[u]:
            if item not in _u_i[user]:
                temp[item] = temp.get(item, 0) + sim / 20
    reco = sorted(temp.items(), key=lambda x:x[1], reverse=True)
    return reco


def cfItem(user, order, cf):
    _i_s = cf.item_sim
    items = order.user_item[user]
    temp = {}

    for item in items:
        for i, sim in _i_s[item]:
            if i not in items:
                temp[i] = temp.get(i, 0) + sim / 20
    reco = sorted(temp.items(), key=lambda x:x[1], reverse=True)
    return reco


def getOrder(order, conn):
    try:
        cur = conn.cursor()
        sql = "SELECT user_id, item_name FROM sam_user_item"
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            order.addOrder(row[0], row[1])
    except MySQLdb.Error, e:
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
    finally:
        conn.close()


def getSim(cf, conn):
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


def getData(cf, order):
    try:
        conn=MySQLdb.connect(host=cnf['host'], port=int(cnf['port']), 
            user=cnf['user'],passwd=cnf['passwd'],db=cnf['dbname'])        
    except MySQLdb.Error, e:
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])

    getSim(cf, conn)
    getOrder(order, conn)
    conn.close()


def writeCFUser(user, reco):
    pass
    
def writeCFItem(user, reco):
    pass
        


def main():
    mycnf.readCnf()

    cf = CF()
    order = Order()

    getData(cf, order)
    
    for user in cf.sim_user.keys():
        reco1 = cfUser(cf, order)
        writeCFUser(user, reco2)

        reco2 = cfItem(cf, order)
        writeCFItem(user, reco2)

if __name__ == '__main__':
    import sys
    main(*sys.argv)
