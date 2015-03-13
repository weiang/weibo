#!/usr/bin/env python
# -*- encoding=utf-8 -*-

import sys
import re
import math
import jieba
import jieba.analyse
from global_config import *

IN_CODEC = u'utf-8'
OUT_CODEC = u'utf-8'

global_config = Global_config()

class Weibo:
    text = u''
    author = u''
    release_time = u''
    
    def __init__(self, text, author, release_time):
        self.text = text
        self.author = author
        self.release_time = release_time

    def url_count(self):
        url_pattern = re.compile(r"http(s)?://")
        return len(re.findall(url_pattern, self.text))

    def tags_weight():
        return 0.0

    def tags_pair_weight():
        return 0.0

    def is_advertisement():
        return False

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

    
def main():
    string = u"https://baidu.com...http://baidu.com...https://"
    w = Weibo(string, 'angwei', '123')
    print w.url_count()

if __name__ == '__main__':
    main()
