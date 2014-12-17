#!/usr/bin/env python
# -*- coding:utf8 -*-

import MySQLdb

conn = MySQLdb.connect(host='localhost',
                       user='root',
                       passwd='',
                       db='test',
                       connect_timeout=3,
                       local_infile=1)

cur = conn.cursor()

cur.execute("select 1, 'foo' union select 2, 'bar'")

results = cur.fetchall()

for row in results:
    print row[0], row[1]

cur.close()
conn.close()
