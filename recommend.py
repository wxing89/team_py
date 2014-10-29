#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pickle
import similarity

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
                    self.userSim[u1] = self.userSim.get(u1, [])
                    continue
                sim = similarity.jaccardIndex(self.userItem[u1], self.userItem[u2])
                if sim > similarity.jaccardMin:
                    self.userSim[u1] = self.userSim.get(u1, [])
                    self.userSim[u1].append((u2, sim))
            self.userSim[u1].sort(key=lambda x:x[1], reverse=True)
            self.userSim[u1] = self.userSim[u1][:self.simSize]

    def getReco(self):
        for u1, simUsers in self.userSim.items():
            temp = {}
            for u2, sim in simUsers:
                for item in self.userItem[u2]:
                    if item not in self.userItem[u1]:
                        temp[item] = temp.get(item, 0) + sim
            self.userReco[u1] = sorted(temp.items(), key=lambda x:x[1], reverse=True)


def main():
    recommend = Recommend()

    orderFile = 'order201408.txt'
    f_reco = open(orderFile)
    for line in f_reco:
        temp = line.split('|')
        user, item = temp[8].strip(), temp[7].strip()
        recommend.addItem(user, item)

    recommend.getSim()
    recommend.getReco()
    

    i = 0
    for user, item in recommend.userItem.items():
        if i < 20:
            print user, '[', 
            for t in item:
                print t, ','
            print ']'
            i += 1
        else:
            break

    i = 0
    for user, sim in recommend.userSim.items():
        if i < 20:
            print user, sim
            i += 1
        else:
            break

    i = 0
    for user, reco in recommend.userReco.items():
        if i < 20:
            print user, '[', 
            for r, s in reco:
                print '(', r, s, ')',
            print ']'
            i += 1
        else:
            break

    with open('recommend.dump', 'w') as f:
        pickle.dump(recommend, f)

if __name__ == '__main__':
	main()
