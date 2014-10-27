#!/usr/bin/env python
# -*- coding:utf8 -*-

import pickle
import random

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

def printTuple(tuples):
    for x, y in tuples:
        print x, y

def printItems(items):
    for i in items:
        print i

def main():
    with open('cf.dump') as f:
        cf = pickle.load(f)

    with open('order.dump') as f:
        order = pickle.load(f)

    _u_i = order.user_item
    _i_u = order.item_user

    _u_s = cf.user_sim
    _i_s = cf.item_sim

    ul = len(_u_s)
    il = len(_i_s)

    n = int(random.random() * ul)
    user = _u_s.keys()[n]
    print user
    print

    print 'Order:'
    printItems(_u_i[user])
    print

    print 'recommend by user:'
    reco = cfUser(user, order, cf)
    printTuple(reco)
    print

    print 'recommend by item'
    reco = cfItem(user, order, cf)
    printTuple(reco)
    print


if __name__ == '__main__':
    main()