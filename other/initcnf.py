#!/usr/bin/env python
# -*- coding:utf8 -*-

import sys

cnf_file = 'init.cnf'

cnf = {}


def initcnf():
    try:
        f = open(cnf_file)
        for line in f:
            if line.strip().startswith('#'):
                continue
            (x, y) = line.split('=', 1)
            cnf[x.strip()] = y.strip()
        f.close()
    except Exception, e:
        print 'Read configure file failed.'
        print e
        sys.exit(128)

def init_cnf():
    f = open(cnf_file)
    for line in f:
        if line.strip().startswith('#'):
            continue
        print line
        (x, y) = line.split('=', 1)
        cnf[x.strip()] = y.strip()
    f.close()


def showcnf():
    """Show cinfiguration details."""
    for k, v in cnf.items():
        print k, '=', v


def setcnf(cnfkey, cnfval):
    """Set 'cnfkey' key to """
    cnf[cnfkey] = cnfval


def getcnf(cnfkey):
    """Get value of cnf 'cnfkey'."""
    return cnf[cnfkey]

init_cnf()