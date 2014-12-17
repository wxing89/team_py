#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import MySQLdb

import conf
from conf import mysql_cnf

from order import Order
from sim import Sim
from logger import logger

from iolib import *


def main():
    conf.init_cnf()

    order = Order()
    conn = MySQLdb.connect(host=mysql_cnf['host'],
                           port=int(mysql_cnf['port']),
                           user=mysql_cnf['user'],
                           passwd=mysql_cnf['passwd'],
                           db=mysql_cnf['db'],
                           connect_timeout=3,
                           local_infile=1)

    mysql_read_order(order, conn)


    sim = Sim(order)
    logger.info('Calculate user similarity ...')
    sim.user_based()
    logger.info('Calculate item similarity ...')
    sim.item_based()

    mysql_write_sim(sim, conn)


if __name__ == '__main__':
    main()
