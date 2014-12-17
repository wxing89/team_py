#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import MySQLdb

import conf
from conf import mysql_cnf
from logger import logger

from order import Order
from sim import Sim
from recommend import Recommend

from iolib import *


def main():
    conf.init_cnf()

    order = Order()
    sim = Sim()
    conn = MySQLdb.connect(host=mysql_cnf['host'],
                           port=int(mysql_cnf['port']),
                           user=mysql_cnf['user'],
                           passwd=mysql_cnf['passwd'],
                           db=mysql_cnf['db'],
                           connect_timeout=3,
                           local_infile=1)

    mysql_read_order(order, conn)
    mysql_read_sim(sim, conn)

    pool = redis.ConnectionPool(host='192.168.9.36', port=6379, db=0, encoding='utf8')
    r = redis.Redis(connection_pool=pool)

    recommend = Recommend(order=order, sim=sim)

    recommend.set_rec(dict())
    recommend.set_rec_by_sim_user(size=20)
    users = recommend.get_rec().keys()
    for u in users:
        redis_write_rec('user:' + u + ':sim_user', recommend.get_user_rec(u), r)

    recommend.set_rec(dict())
    recommend.set_rec_by_sim_item(size=20)
    users = recommend.get_rec().keys()
    for u in users:
        redis_write_rec('user:' + u + ':sim_item', recommend.get_user_rec(u), r)


if __name__ == '__main__':
    main()