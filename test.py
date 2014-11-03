#!/usr/bin/env python
# -*- coding:utf8 -*-

from cf import CF
import pickle
import random

def main():
    with open('cf.dump') as f:
        cf = pickle.load(f)
    
    with open('user_sim.dat', 'w') as f:
        for user in cf.user_sim:
            for u, sim in cf.user_sim[user]:
                f.write('|'.join([user, u, str(sim), '\n']))

    with open('item_sim.dat', 'w') as f:
        for item in cf.item_sim:
            for i, sim in cf.item_sim[item]:
                f.write('|'.join([item, i, str(sim), '\n']))


if __name__ == '__main__':
    main()