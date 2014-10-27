#!/usr/bin/env python
# -*- coding:utf8 -*-

from recommend import Recommend
import pickle
import random

def main():
    with open('recommend.dump') as f:
        reco = pickle.load(f)

    num = len(reco.userItem)

    sig = 1
    while sig:
        n = int(random.random() * num)

        user = reco.userItem.keys()[n]
        print user

        print 'ordered:', 
        for item in reco.userItem[user]:
            print item
        print
        print

        print 'similarity:', reco.userSim[user]
        print
        print

        print 'recommend:', 
        for u, r in reco.userReco[user]:
            print u, r
        print
        print
        
        sig = input('0 - Exit\n1 - Continue:')


if __name__ == '__main__':
    main()