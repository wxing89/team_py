#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import sys
import pickle
import MySQLdb
import redis

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
        try:
            for i, sim in _i_s[item]:
                if i not in items:
                    temp[i] = temp.get(i, 0) + sim / 20
        except:
            pass
    reco = sorted(temp.items(), key=lambda x:x[1], reverse=True)
    return reco


def getOrder(order, conn):
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
    finally:
        cur.close()


def getData(cf, order):
    try:
        conn=MySQLdb.connect(host=cnf['host'], port=int(cnf['port']), 
            user=cnf['user'],passwd=cnf['passwd'],db=cnf['dbname'])        
    except MySQLdb.Error, e:
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])

    getSim(cf, conn)
    getOrder(order, conn)
    conn.close()


def writeCFUser(user_id, reco, r):
    k = 'user:' + user_id + ':cfuser'
    for (i, s) in reco:
        r.zadd(k, i, s)

    
def writeCFItem(user_id, reco, r):
    k = 'user:' + user_id + ':cfitem'
    for (i, s) in reco:
        r.zadd(k, i, s)
        


def main():
    mycnf.readCnf()

    cf = CF()
    order = Order()

    getData(cf, order)
    
    pool = redis.ConnectionPool(host='192.168.9.36', port=6379, db=0, encoding='utf8')
    r = redis.Redis(connection_pool=pool)

    for user in cf.user_sim.keys():
        reco1 = cfUser(user, order, cf)
        writeCFUser(user, reco1, r)

        reco2 = cfItem(user, order, cf)
        writeCFItem(user, reco2, r)

if __name__ == '__main__':
    main()
