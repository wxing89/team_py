#!/usr/bin/env python
# -*- coding:utf-8 -*-

from order import Order
import sims


class Similaryity():
    """
    user_sim: user similarity matrix
        {userA: [(userB, 0.56), (userC, 0.38), ...]}
        {userB: [(userD, 0.76), (userA, 0.56), ...]}
        ...

    item_sim: item similarity matrix
        {itemA: [(itemB, 0.56), (itemC, 0.38), ...]}
        {itemB: [(itemD, 0.76), (itemA, 0.56), ...]}
        ...
    """

    __sims = {
        'jaccard': sims.jaccardIndex,
        'cosine' : sims.cosineSimilarity,
        'pearson': sims.pearsonIndex
    }

    def __init__(self, order=None):
        self.order = order or Order()
        self.user_sim = {}
        self.item_sim = {}

    def get_user_sim(self):
        return self.user_sim

    def set_user_sim(self, user_sim):
        self.user_sim = user_sim

    def get_item_sim(self, item_sim):
        return self.item_sim

    def set_item_sim(self, item_sim):
        self.item_sim = item_sim

    def get_user_sim_score(self, user1, user2):
        try:
            return self.user_sim[user1][user2]
        except IndexError:
            return 0

    def set_user_sim_score(self, user1, user2, score):
        self.user_sim.setdefault(user1, {})
        self.user_sim[user1][user2] = score

    def add_user_sim_score(self, user1, user2, score):
        self.user_sim.setdefault(user1, {})
        self.user_sim[user1].setdefault(user2, score)

    def get_item_sim_score(self, item1, item2):
        try:
            return self.item_sim[item1][item2]
        except IndexError:
            return 0

    def set_item_sim_score(self, item1, item2, score):
        self.item_sim.setdefault(item1, {})
        self.item_sim[item1][item2] = score

    def add_item_sim_score(self, item1, item2, score):
        self.item_sim.setdefault(item1, {})
        self.item_sim[item1].setdefault(item2, score)

    def user_based(self, simFun='jaccard', userSize=20):
        """
        Calculate user similarity.

        :rtype : None
        :param simFun: similarity algorithm: 'jaccard', 'cosine', 'pearson'
        :param userSize: user similarity set size
        :return: None
        """
        logger.info('calculate user similarity by {0:s} similarity'.format(simFun))
        if not self.order:
            return

        simMethod = self.__sims[simFun]
        _u_i = self.order.user_item
        _u_s = self.user_sim

        for u1 in _u_i.keys():
            for u2 in _u_i.keys():
                if u1 is u2:
                    _u_s[u1] = _u_s.get(u1, [])
                    continue
                sim = simMethod(_u_i[u1], _u_i[u2])
                if sim > 0:
                    _u_s[u1] = _u_s.get(u1, [])
                    _u_s[u1].append((u2, sim))
            _u_s[u1].sort(key=lambda x:x[1], reverse=True)
            _u_s[u1] = _u_s[u1][:userSize]

    def item_based(self, simFun='cosine', itemSize=20):
        """
        Calculate item similarity.

        :rtype : None
        :param simFun: similarity algorithm: 'jaccard', 'cosine', 'pearson'
        :param userSize: item similarity set size
        :return: None
        """
        if not self.order:
            return

        simMethod = self.__sims[simFun]
        _i_u = self.order.item_user
        _i_s = self.item_sim

        for i1 in _i_u.keys():
            for i2 in _i_u.keys():
                if i1 is i2:
                    _i_s[i1] = _i_s.get(i1, [])
                    continue
                sim = simMethod(_i_u[i1], _i_u[i2])
                if sim > 0:
                    _i_s[i1] = _i_s.get(i1, [])
                    _i_s[i1].append((i2, sim))
            _i_s[i1].sort(key=lambda x:x[1], reverse=True)
            _i_s[i1] = _i_s[i1][:itemSize]
