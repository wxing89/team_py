#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pickle

import order

class Recommend():
    """
    userItem: user - item matrix, like
        {userA: (item1, item2, item3, ...)}
        {userB: (item2, item4, item5, ...)}
        ...

    userSim: user similarity matrix, like
        {userA: [(userB, 0.56), (userC, 0.38), ...]}
        {userB: [(userD, 0.76), (userA, 0.56), ...]}
        ...

    userReco: user - recommendation matrix, like
        {userA: [(reco1: 9.23), (reco2, 8.34), ...]}
        {userB: [(reco1: 7.11), (reco2, 4.11), ...]}
        ...
    """
    def __init__(self, size=20):
        self.simSize = size
        self.userItem = {}
        self.userSim  = {}
        self.userReco = {}

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
                self.userSim[u1].append((u2, sim))
            self.userSim[u1].sort(key=lambda x:x[1], reverse=True)
            self.userSim[u1] = userSim[u1][:self.simSize]

    def getReco(self):
        for u1, simUsers in self.userSim.items():
            for u2, sim in simUsers:
                temp = {}
                for item in self.userItem[u2]:
                    temp[u2] = temp.get(u2, 0) + sim
            self.userReco[u1] = sorted(temp.items(), key=lambda x:x[1], reverse=True)


def main():
    temp = order.Order()
    with open('order.dump') as f:
        temp = pickle.load(f)

    reco = Recommend()
    reco.userSim = temp.userSim
    reco.userItem = temp.userItem
    reco.getReco()

    i = 0
    for user, reco in temp.userReco.items():
        if i < 20:
            print user, reco
            i += 1
        else:
            break


if __name__ == '__main__':
	main()
