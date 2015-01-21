#!/usr/bin/env python
# -*- coding:utf8 -*-

from order import Order
from similarity import Similaryity
from rule import Rule
from rank import Rank

class Recommend():
    def __init__(self, order=None, sim=None, rule=None, rank=None):
        self.order = order or Order()
        self.sim = sim or Similaryity()
        self.rule = rule or Rule()
        self.rank = rank or Rank()
        self.rec = {}

    def get_order(self):
        return self.order

    def get_sim(self):
        return self.sim

    def get_rule(self):
        return self.rule

    def get_rank(self):
        return self.rank

    def get_rec(self):
        return self.rec

    def set_order(self, order):
        self.order = order

    def set_sim(self, sim):
        self.sim = sim

    def set_rule(self, rule):
        self.rule = rule

    def set_rank(self, rank):
        self.rank = rank

    def set_rec(self, rec):
        self.rec = rec

    def get_user_rec(self, user):
        return self.rec.get(user, {})

    def set_user_rec(self, user, r):
        self.rec[user] = r

    def get_rec_score(self, user, item):
        try:
            return self.rec[user][item]
        except IndexError:
            return 0

    def set_rec_score(self, user, item, score):
        self.rec.setdefault(user, {})
        self.rec[user][item] = score

    def by_knowledge(self):
        pass

    def by_multi(self):
        pass

    def by_sim_user(self, user, size=20):
        """

        :param user: user id 
        :param size: return set size
        :return: recommend items set
        """
        _u_i = self.order.user_item
        sim_users = self.sim.user_sim[user]
        temp = {}
    
        for u, s in sim_users:
            for item in _u_i[u]:
                if item not in _u_i[user]:
                    temp[item] = temp.get(item, 0) + s / size
        r = sorted(temp.items(), key=lambda x:x[1], reverse=True)
        return r[:size]

    def by_sim_item(self, user, size=20):
        """

        :param user: user id
        :param size: return set size
        :return: recommend items set
        """
        _i_s = self.sim.item_sim
        items = self.order.user_item[user]
        temp = {}
    
        for item in items:
            try:
                for i, s in _i_s[item]:
                    if i not in items:
                        temp[i] = temp.get(i, 0) + s / size
            except:
                pass
        r = sorted(temp.items(), key=lambda x:x[1], reverse=True)
        return r[:size]

    def by_rule(self, item, size=10):
        pass

    def by_rank(self, area='all', size=10):
        pass

    def set_rec_by_sim_user(self, size=20):
        for u in self.sim.user_sim.keys():
            r = self.by_sim_user(u, size)
            self.set_user_rec(u, r)

    def set_rec_by_sim_item(self, size=20):
        for u in self.sim.user_sim.keys():
            r = self.by_sim_item(u, size)
            self.set_user_rec(u, r)