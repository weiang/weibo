#! /usr/bin/env python
# -*- encoding: utf-8 -*-

'''
        Usage: python ./gen_test_weibo.py <user weibo file> [out file]
                   Genrate test weibo set from user's weibo list
                   <user weibo file>: <uid>\t<weibo 1>\t<weibo 2>...\t...\t<weibo n>
'''

import os
import sys
import json
import codecs
import chardet

IN_CODEC = u'utf-8'
OUT_CODEC = u'utf-8'

if __name__ == u'__main__':
        if len(sys.argv) < 2:
            print __doc__
            sys.exit(-1)

        infd = codecs.open(sys.argv[1], u'r', IN_CODEC)
        if len(sys.argv) >= 3:
                outfd = codecs.open(sys.argv[2], u'w', OUT_CODEC)
        else:
                outfd = sys.stdout

        for line in infd:
            ls = line.strip(u' \t\n').split(u'\t')
            uid = ls[0]
            weibos = ls[1:]
            for weibo in weibos:
                weibo = weibo.encode('utf-8')
                weibo = weibo.strip(' \t\n').replace('\x0a2f', '')
#                print chardet.detect(weibo)                    
                info = '0\t' + weibo + '\n'
                if len(sys.argv) >= 3:
                    info = info.decode('utf-8')
                outfd.write(info)

        infd.close()
        if len(sys.argv) >=3:
                outfd.close()


