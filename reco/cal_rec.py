#!/usr/bin/env python
# -*- coding:utf8 -*-

import MySQLdb

from mycnf import MyCnf
from mylog import MyLog

from order import Order
from similarity import Similaryity
from recommend import Recommend

from iolib import *

LOG_FILE = "rec.log"
CFG_FILE = "rec.ini"


def main():
    mylog = MyLog(LOG_FILE)
    mylog.info("PROGRAM BEGIN ...")

    mycnf = MyCnf(CFG_FILE)
    mysql_cnf = mycnf.mysql_cnf

    order = Order()
    sim = Similaryity()
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

    mylog.info("write rec by sim_user to redis ...")
    recommend.set_rec(dict())
    recommend.set_rec_by_sim_user(size=20)
    users = recommend.get_rec().keys()
    for u in users:
        redis_write_rec('user:' + u + ':sim_user', recommend.get_user_rec(u), r)

    mylog.info("write rec by sim_item to redis ...")
    recommend.set_rec(dict())
    recommend.set_rec_by_sim_item(size=20)
    users = recommend.get_rec().keys()
    for u in users:
        redis_write_rec('user:' + u + ':sim_item', recommend.get_user_rec(u), r)

    mylog.info("PROGRAM FINISHED.")


if __name__ == '__main__':
    main()