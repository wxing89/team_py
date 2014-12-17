#!/usr/bin/env python
# -*- coding:utf-8 -*-

from order import Order
import similarity

from logger import logger


class Sim():
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
        'jaccard': similarity.jaccardIndex,
        'cosine' : similarity.cosineSimilarity,
        'pearson': similarity.pearsonIndex
    }

    def __init__(self, order=None):
        self.order = order or Order()
        self.user_sim = {}
        self.item_sim = {}

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
