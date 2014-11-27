#!/usr/bin/python2.7
# -*- coding:utf8 -*-

from order import Order
from cf import CF


class CFRecommend():
    def __init__(self, order=None, cf=None):
        self.order = order or Order()
        self.cf = cf or CF()
        self.cfuser = {}
        self.cfitem = {}

    def cf_recommend():
        """ Recommend by CF
        """
        for user in self.cf.user_sim.keys():
            cf_user(user)
            cf_user(item)

    def cf_user(user):
        _u_i = self.order.user_item
        sim_users = self.cf.user_sim[user]
        temp = {}

        for u, sim in sim_users:
            try:
                for item in _u_i[u]:
                    if item not in _u_i[user]:
                        temp[item] = temp.get(item, 0) + sim / 20
            except KeyError:
                pass
        reco = sorted(temp.items(), key=lambda x:x[1], reverse=True)
        self.cfuser[user] = reco

    def cf_item(user):
        _i_s = self.cf.item_sim
        items = self.order.user_item[user]
        temp = {}

        for item in items:
            try:
                for i, sim in _i_s[item]:
                    if i not in items:
                        temp[i] = temp.get(i, 0) + sim / 20
            except KeyError:
                pass
        reco = sorted(temp.items(), key=lambda x:x[1], reverse=True)
        self.cfitem[user] = reco

