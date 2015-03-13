#!/usr/bin/env python
# -*- coding=utf-8 -*-


'''
    Usage: python ./gen_train_data.py <data set> [tag dict] [tag_pair dict] 
           Generate data for svm training
'''

from weibo_text import *
from dictionary import *

def usage():
    print __doc__

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(-1)
    
    data_set = sys.argv[1]
    f_tag_dict = u'tag_weight.dict'
    f_tag_pair_dict = u'tag_pair_weight.dict'
    if len(sys.argv) >= 3:
        f_tag_dict = sys.argv[2]
    if len(sys.argv) >= 4:
        f_tag_pair_dict = sys.argv[3]

    tag_weight_dict = load_tag_weight_dict(f_tag_dict)
    tag_weight_pair_dict = load_tag_pair_weight_dict(f_tag_pair_dict)
