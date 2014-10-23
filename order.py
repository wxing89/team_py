#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import similarity
import pickle

class Order():
    """
    userSim: user similarity matrix, like
        {userA: [(userB, 0.56), (userC, 0.38) ...]}
        {userB: [(userD, 0.76), (userA, 0.56) ...]}
        ...

    userItem: user - item matrix, like
        {userA: (item1, item2, item3)}
        {userB: (item2, item4, item5)}
        ...
    """
    def __init__(self, size=20):
        self.simSize = size
        self.userSim = {}
        self.userItem = {}

    def addItem(self, user, item):
        self.userItem[user] = self.userItem.get(user, set())
        self.userItem[user].add(item)

    def getSim(self):
        for u1 in self.userItem.keys():
            for u2 in self.userItem.keys():
                if u1 is u2:
                    continue
                sim = similarity.jaccardIndex(self.userItem[u1], self.userItem[u2])
                self.userSim[u1] = self.userSim.get(u1, [])
                if len(self.userSim[u1]) < self.simSize:
                    self.userSim[u1].append((u2, sim))
                else:
                    if sim > self.userSim[u1][self.simSize - 1][1]:
                        self.userSim[u1].append((u2, sim))
                        self.userSim[u1].sort(key=lambda x:x[1], reverse=True)
                        self.userSim[u1].pop()

def main():
    order = Order()

    orderFile = 'D:\\user\\order\\order201408.txt'
    f_order = open(orderFile)
    for line in f_order:
        temp = line.split('|')
        user, item = temp[8].strip(), temp[7].strip()
        order.addItem(user, item)

    order.getSim()

    i = 0
    for user, item in order.userItem.items():
        if i < 20:
            print user, item
            i += 1
        else:
            break

    i = 0
    for user, sim in order.userSim.items():
        if i < 20:
            print user, sim
            i += 1
        else:
            break

    with open('order.dump', 'w') as f:
        pickle.dump(order, f)

if __name__ == '__main__':
    main()