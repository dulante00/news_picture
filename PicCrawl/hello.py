#!/usr/bin/env python
#_*_coding:utf-8_*_

'a test module'

__author__='liming'
import sys

def hello():
    args=sys.argv
    if len(args)==1:
        print(args)
    elif len(args)==2:
        print('hello',args)
    else:
        print('too many args')
if __name__=='__main__':
    hello()
    print(__doc__)