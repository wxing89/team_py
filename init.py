#!/usr/bin/env python
# -*- coding:utf8 -*-

import pickle

from order import Order
from cf import CF

def readOrder(order, filename='order201408'):
    f = open(filename)
    for line in f:
        temp = line.split('|')
        user, item = temp[0].strip(), temp[1].strip()
        order.addOrder(user, item)


def main():
    order = Order()
    readOrder(order)

    with open('order.dump', 'w') as f:
        pickle.dump(order, f)

    cf = CF(order)
    cf.userBased()
    cf.itemBased()

    with open('cf.dump', 'w') as f:
        pickle.dump(cf, f)


if __name__ == '__main__':
    main()
