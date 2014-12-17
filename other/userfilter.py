#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re

def userFilter(orderFile, filterFile):
    f_filter = open(filterFile, 'a')
    try:
        with open(orderFile) as f_order:
            for line in f_order:
                tmp_list = line.split('|')
                user, item = tmp_list[8].strip(), tmp_list[7].strip()
                if item != '' and item != 'null' and user != '':
                    f_filter.write(line)
    except IOError as ioe:
        print ioe
    except IndexError as ide:
        pass
    finally:
        f_filter.close()

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
    order_dir = 'D:\\user\\order'
    filter_file = 'D:\\user\\order\\order201408.dat'
    o_file = 'D:\\user\\order\\order201408.txt'

    pattern = re.compile('order201408[0-3][0-9]\.txt')

    if os.path.exists(filter_file):
        os.remove(os.path.join(order_dir, filter_file))

    for order_file in os.listdir(order_dir):
        if re.match(pattern, order_file):
            print order_file
            userFilter(os.path.join(order_dir, order_file), filter_file)

    u_dict = counter(filter_file, p_field=9)
    u_list = filter(filter_file, u_dict, p_field=9)

    with open(o_file, 'w') as f:
        for u_item in u_list:
            f.write(u_item)

if __name__ == '__main__':
    main()