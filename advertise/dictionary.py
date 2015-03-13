#!/usr/bin/env python
# -*- encoding=utf-8 -*-

import codecs

IN_CODEC = u'utf-8'
OUT_CODEC = u'utf-8'

def gen_dict(dic, filename):
    fd = codecs.open(filename, u'w', OUT_CODEC)

    for key, value in dic.items():
        fd.write(u'%s\t%f\n' %(key, value))

    fd.close()

def gen_tag_weight_dict(tag_dict, filename=u'tag_weight.dict'):
    gen_dict(tag_dict, filename)

def gen_tag_pair_weight_dict(tag_pair_dict, filename=u'tag_pair_weight.dict'):
    gen_dict(tag_pair_dict, filename)

def load_dict(filename):
    fd = codecs.open(filename, u'r', IN_CODEC)

    tag_dict = {}
    for line in fd:
        line = line.strip(u' \t\n')
        try:
            tag, weight = line.split(u'\t')
        except:
            continue
        tag_dict[tag] = float(weight)

    fd.close()
    return tag_dict

def load_tag_weight_dict(filename=u'tag_weight.dict'):
    return load_dict(filename)

def load_tag_pair_weight_dict(filename=u'tag_pair_weight.dict'):
    return load_dict(filename)
