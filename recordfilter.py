#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os

def counter(p_file, p_field=1, p_split='|'):
    p_dict = dict()
    with open(p_file) as fp:
        for line in fp:
            field = line.split(p_split)[p_field - 1]
            p_dict[field] = p_dict.get(field, 0) + 1
    return p_dict

def filter(p_file, p_dict, p_field=1, p_split='|', p_num=10):
    p_line = []
    with open(p_file) as fp:
        for line in fp:
            if p_dict[line.split(p_split)[p_field - 1]] >= p_num:
                p_line.append(line)

    return p_line

def main():
    p_file = 'D:\\user\\order\\order20140802.txt'
    p_dict = counter(p_file, 9)

    p_line = filter(p_file, p_dict, 9, p_num=50)
    for line in p_line:
        print line.split('|')[7]


if __name__ == '__main__':
    main()