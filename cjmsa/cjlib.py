#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import MySQLdb

from cjcnf import CJCnf
from cjlog import CJLog

DataDir = 'data'

def file_read_order(order, filename='order201408'):
    CJLog.info('Read user-item data from file %s ...'.format(filename))
    f = open(filename)
    for line in f:
        temp = line.split('|')
        user, item = temp[0].strip(), temp[1].strip()
        order.addOrder(user, item)


def mssql_read_order(order, conn):
    CJLog.info('Read user-item data from mssql ...')
    sql = "SELECT * FROM ex_user_item"
    try:
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            user = row[1]
            item = row[2]
            order.add_order(user, item)
        cur.close()
    except MySQLdb.Error, e:
        CJLog.error('mssql Error {0:d}: {1:s}'.format(e.args[0], e.args[1]))


def file_write_sim(sim, split='|'):
    file_write_sim_user(sim, filename=os.path.join(CJCnf.file_cnf['directory'], 'user_sim.dat'), split=split)
    file_write_sim_item(sim, filename=os.path.join(CJCnf.file_cnf['directory'], 'item_sim.dat'), split=split)


def file_write_sim_user(sim, filename='user_sim.dat', split='|'):
    CJLog.info('Write user-sim data into file {0:s}'.format(filename))
    with open(filename, 'w') as f:
        for user in sim.user_sim:
            for u, s in sim.user_sim[user]:
                f.write(split.join([user, u, str(s), '\n']))


def file_write_sim_item(sim, filename='item_sim.dat', split='|'):
    CJLog.info('Write item-sim data into file {0:s}'.format(filename))
    with open(filename, 'w') as f:
        for item in sim.item_sim:
            for i, s in sim.item_sim[item]:
                f.write(split.join([item, i, str(s), '\n']))


def file_read_sim(sim, split='|'):
    """
    :param sim: instance of class Sim()
    :param filename: file source
    :param split: file line split
    """
    file_read_sim_user(sim, filename=os.path.join(CJCnf.file_cnf['directory'], 'user_sim.dat'), split=split)
    file_read_sim_item(sim, filename=os.path.join(CJCnf.file_cnf['directory'], 'item_sim.dat'), split=split)


def file_read_sim_user(sim, filename='user_sim.dat', split='|'):
    CJLog.info('Read user-sim data from file {0:s}'.format(filename))
    with open(filename) as f:
        for line in f:
            u1, u2, s = line.split(split)
            sim.add_user_sim_score(u1, u2, s)


def file_read_sim_item(sim, filename='item_sim.dat', split='|'):
    CJLog.info('Read item-sim data from file {0:s}'.format(filename))
    with open(filename) as f:
        for line in f:
            i1, i2, s = line.split(split)
            sim.add_item_sim_score(i1, i2, s)


def mssql_read_sim(sim, conn):
    mssql_read_sim_user(sim, conn)
    mssql_read_sim_item(sim, conn)


def mssql_write_sim(sim, conn):
    mssql_write_sim_user(sim, conn)
    mssql_write_sim_item(sim, conn)


def mssql_read_sim_user(sim, conn):
    CJLog.info('Read user similarity data from mssql ...')
    cur = conn.cursor()
    try:
        sql = "SELECT user_1, user_2, sim FROM sim_user";
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            u1, u2, s = row[0], row[1], row[2]
            sim.user_sim[u1] = sim.user_sim.get(u1, [])
            sim.user_sim[u1].append((u2, s))
    except MySQLdb.Error, e:
        CJLog.error('mssql Error {0:d}: {1:s}'.format(e.args[0], e.args[1]))
    finally:
        cur.close()


def mssql_read_sim_item(sim, conn):
    CJLog.info('Read item similarity data from mssql ...')
    cur = conn.cursor()
    try:
        sql = "SELECT item_1, item_2, sim FROM sim_item";
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            i1, i2, s = row[0], row[1], row[2]
            sim.item_sim[i1] = sim.item_sim.get(i1, [])
            sim.item_sim[i1].append((i2, s))
    except MySQLdb.Error, e:
        CJLog.error('mssql Error {0:d}: {1:s}'.format(e.args[0], e.args[1]))
    finally:
        cur.close()


def mssql_write_sim_user(sim, conn):
    if not os.path.isdir(DataDir):
        os.mkdir(DataDir)
    CJLog.info("Write user similarity to mssql ...")
    file_write_sim_user(sim, os.path.join(DataDir, 'user_sim.dat'))

    sql = u"LOAD DATA LOCAL INFILE '{0:s}' REPLACE INTO TABLE sim_user FIELDS TERMINATED BY '|' \
    LINES TERMINATED BY '\\n'".format(os.path.join(DataDir, 'user_sim.dat'))
    cur = conn.cursor()
    try:
        CJLog.info('Write user-sim data into mssql ...')
        CJLog.info('EXECUTE SQL - {0:s}'.format(sql))
        cur.execute(sql)
        conn.commit()
    except MySQLdb.Error, e:
        CJLog.error('mssql Error {0:d}: {1:s}'.format(e.args[0], e.args[1]))
        conn.rollback()
    finally:
        cur.close()


def mssql_write_sim_item(sim, conn):
    if not os.path.isdir(DataDir):
        os.mkdir(DataDir)
    CJLog.info("Write item similarity to mssql ...")
    file_write_sim_item(sim, os.path.join(DataDir, 'item_sim.dat'))

    sql = u"LOAD DATA LOCAL INFILE '{0:s}' REPLACE INTO TABLE sim_item FIELDS TERMINATED BY '|' \
    LINES TERMINATED BY '\\n'".format(os.path.join(DataDir, 'item_sim.dat'))
    cur = conn.cursor()
    try:
        CJLog.info('Write item-sim data into mssql ...')
        CJLog.info("EXECUTE SQL - {0:s}".format(sql))
        cur.execute(sql)
        conn.commit()
    except MySQLdb.Error, e:
        CJLog.error('mssql Error {0:d}: {1:s}'.format(e.args[0], e.args[1]))
        conn.rollback()
    finally:
        cur.close()


