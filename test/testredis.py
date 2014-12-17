#!/usr/bin/env python
# -*- coding:utf8 -*-

import redis

pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db=9)

r = redis.Redis(connection_pool=pool)

fo='foo'
ba='bar'
r.zadd('user:1:cf', 'foo', 0.9, 'bar', 0.5)
r.zadd('user:2:cf', fo=0.4, ba=0.6)

print r.zrange('user:1:cf', 0, -1)
print r.zrange('user:2:cf', 0, -1, withscores=1)

print r.flushdb()
