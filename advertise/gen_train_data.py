#!/usr/bin/env python
# -*- coding=utf-8 -*-

'''
    Usage: python ./gen_train_data.py <data set> <libsvm format file> [tag dict] [tag_pair dict] 
           Generate data for svm training
'''

import sys
import re
import math
import codecs
import jieba
import jieba.analyse
from global_config import *
from weibo_text import *
from dictionary import *

IN_CODEC = u'utf-8'
OUT_CODEC = u'utf-8'

global_config = Global_config()

class Weibo:
    text = u''
    author = u''
    release_time = u''
    is_ad = False

    def __init__(self, text, author=u'', release_time=u''):
        self.text = text
        self.author = author
        self.release_time = release_time

    def url_count(self):
        url_pattern = re.compile(r"http(s)?://")
        return len(re.findall(url_pattern, self.text))

    def tags_weight(self):
        result = .0
        tags = jieba.analyse.extract_tags(self.text)
        for tag in tags:
            if tag in tag_weight_dict:
                result += tag_weight_dict[tag]
        return result 

    def tags_pair_weight(self):
        result = .0
        tags = jieba.analyse.extract_tags(self.text)

        for i in range(0, len(tags)-1):
            for j in range(i+1, len(tags)):
                key = pair_tags(tags[i], tags[j])
                if key in tag_pair_weight_dict:
                    result += tag_pair_weight_dict[key]
        return result 

    def is_advertisement(self):
        return self.is_ad
    
    def output_features(self, fd):
        if self.is_advertisement():
            label = '1'
        else:
            label = '0'
        tw = self.tags_weight()
        tpw = self.tags_pair_weight()
        uc = self.url_count()

        ostring = '%s 1:%f 2:%f 3:%d\n' %(label, tw, tpw, uc)
        fd.write(ostring)

# Compute the rate of advertisement in a Weibo list
def advertisement_rate(weibo_list):
    advertisement_count = 0
    for weibo in weibo_list:
        if weibo.is_advertisement():
            advertisement += 1
    return float(advertisement_count) / len(weibo_list)

class User:
    followers = {}
    followees = {}
    released_weibos = {}

    def get_follower_count(self):
        return followers.len()

    def get_followee_count(self):
        return followee.len() 

    def reputation():
        result = float(self.get_follower_count())
        result = result / (result + self.get_followee_count())
        return result

    def average_non_active_weibo_rate(self, day_count):
        result = 0.0
        return result

    def weibo_repeatation_rate(self):
        return 0.0

    def is_advertiser(self):
        rate = advertisement_rate(self.released_weibos)
        if rate > global_conf.advertisement_threshold:
            return True
        else:
            return False

def load_weibo_data(filename):
    fd = codecs.open(filename, 'r', IN_CODEC)

    weibos = []
    for line in fd:
        line = line.strip(u' \t\n')
        flag, text = line.split(u'\t')
        w = Weibo(text)
        if flag == u'1':
            w.is_ad = True
        weibos.append(w)
    return weibos

def usage():
    print __doc__

# def extract_weibo_text_feature():

if __name__ == '__main__':
#    global tag_weight_dict, tag_pair_weight_dict
    if len(sys.argv) < 3:
        usage()
        sys.exit(-1)
    
    data_set = sys.argv[1]
    output_file = sys.argv[2]
    f_tag_dict = u'tag_weight.dict'
    f_tag_pair_dict = u'tag_pair_weight.dict'

    if len(sys.argv) >= 4:
        f_tag_dict = sys.argv[3]
    if len(sys.argv) >= 5:
        f_tag_pair_dict = sys.argv[4]

    of = codecs.open(output_file, 'w', OUT_CODEC)
    tag_weight_dict = load_tag_weight_dict(f_tag_dict)
    tag_pair_weight_dict = load_tag_pair_weight_dict(f_tag_pair_dict)
    weibos = load_weibo_data(data_set)

    weibo_features = {}
    for weibo in weibos:
        feature_list = weibo.output_features(of)

    of.close()
