#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import MySQLdb

from mycnf import MyCnf
from mylog import MyLog

from order import Order
from similarity import Similaryity

from iolib import *

CNF_FILE = "sim.ini"
LOG_FILE = "sim.log"


def main():
    mylog = MyLog(LOG_FILE)

    mylog.info("PROGRAM BEGIN ...")

    mycnf = MyCnf(CNF_FILE)
    mysql_cnf = mycnf.mysql_cnf

    order = Order()
    conn = MySQLdb.connect(host=mysql_cnf['host'],
                           port=int(mysql_cnf['port']),
                           user=mysql_cnf['user'],
                           passwd=mysql_cnf['passwd'],
                           db=mysql_cnf['db'],
                           connect_timeout=3,
                           local_infile=1)

    mysql_read_order(order, conn)

    sim = Similaryity(order)
    mylog.info('Calculate user similarity ...')
    sim.user_based()
    mylog.info('Calculate item similarity ...')
    sim.item_based()

    mysql_write_sim(sim, conn)

    mylog.info("PROGRAM FINISHED.")

if __name__ == '__main__':
    main()
