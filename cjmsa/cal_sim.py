#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import MySQLdb

from cjcnf import CJCnf
from cjlog import CJLog

from order import Order
from similarity import Similaryity

from cjlib import *


CNF_FILE = "cjmsa.ini"
LOG_FILE = "cjmsa.log"


def main():
    cjlog = CJLog(LOG_FILE)

    cjlog.info("PROGRAM BEGIN ...")

    cjcnf = CJCnf(CNF_FILE)
    mssql_cnf = cjcnf.mssql_cnf

    order = Order()
    conn = MySQLdb.connect(host=mssql_cnf['host'],
                           port=int(mssql_cnf['port']),
                           user=mssql_cnf['user'],
                           passwd=mssql_cnf['passwd'],
                           db=mssql_cnf['db'],
                           connect_timeout=3,
                           local_infile=1)

    mssql_read_order(order, conn)

    sim = Similaryity(order)
    cjlog.info("Calculate users' similarity ...")
    sim.user_based()
    cjlog.info("Calculate courses' similarity ...")
    sim.item_based()

    mssql_write_sim_item(sim, conn)

    CJLog.info("PROGRAM FINISHED.")

if __name__ == '__main__':
    main()
