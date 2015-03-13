#!/usr/bin/env python
# -*- encoding=utf-8 -*-

import sys
import re
import math
import jieba
import jieba.analyse
import Levenshtein

IN_CODE = u'utf-8'
OUT_CODE = u'utf-8'

class Global_config:
    advertisement_threshold = 0.5
    advertisement_frequent_tags = 5
    advertisement_frequent_tags_pair = 5

global_config = Global_config()

# print global_config.advertisement_threshold

def weibo_tag_frequent(weibos):
	tag_frequent = {}
	for weibo in weibos:
		tags = jieba.analyse.extract_tags(weibo)
		for tag in tags:
			if tag not in tag_frequent:
				tag_frequent[tag] = 0
				# print 'Tag: ', tag.encode(OUT_CODE)
		weibo_segments = jieba.cut(weibo)
		for segment in weibo_segments:
			if segment in tag_frequent:
				tag_frequent[segment] += 1

	return tag_frequent

def weibo_tag_weight(advertisement_weibos, normal_weibos):
	adv_tag_frequent = weibo_tag_frequent(advertisement_weibos)
	normal_tag_frequent = weibo_tag_frequent(normal_weibos)

	result = {}
	for tag in adv_tag_frequent:
		if tag not in normal_tag_frequent:
			result[tag] = 1.0
		else:
			result[tag] = float(adv_tag_frequent[tag] - normal_tag_frequent[tag]) / \
                                (adv_tag_frequent[tag] + normal_tag_frequent[tag])

	return result

def pair_tags(str1, str2):
	str1 = str1.strip(u' \n\t')
	str2 = str2.strip(u' \n\t')

	result = u''
	if str1 < str2:
		result = str1 + u'###' + str2
	else:
		result = str2 + u'###' + str1

	return result

def depair_tags(tag_pair):
	tag_pair = tag_pair.strip(u' \n\t')
	tags = tag_pair.split(u'###')
	return (tags[0], tags[1])

def weibo_tag_pair_frequent(weibos):
	weibo_tag_pair_frequent = {}
	for weibo in weibos:
		tags = jieba.analyse.extract_tags(weibo)
		for i in range(len(tags)):
			for j in range(i+1, len(tags)):
				key = pair_tags(tags[i], tags[j])
				if key not in weibo_tag_pair_frequent:
					weibo_tag_pair_frequent[key] = 0
				weibo_tag_pair_frequent[key] += 1
	
	return weibo_tag_pair_frequent

def weibo_tag_pair_weight(advertisement_weibos, normal_weibos):
	adv_tag_pair_frequent = weibo_tag_pair_frequent(advertisement_weibos)
	normal_tag_pair_frequent = weibo_tag_pair_frequent(normal_weibos)

	result = {}
	for tag_pair in adv_tag_pair_frequent:
		if tag_pair not in normal_tag_pair_frequent:
			result[tag_pair] = 1.0
		else:
			result[tag_pair] = float(adv_tag_pair_frequent[tag_pair] - normal_tag_pair_frequent[tag_pair]) / \
                                (adv_tag_pair_frequent[tag_pair] + normal_tag_pair_frequent[tag_pair])

	return result

def lev_distance(text1, text2):
	return Levenshtein.distance(text1, text2)

def lev_similarity(text1, text2):
	ld = lev_distance(text1, text2)
	return 1 - float(ld) / max(len(text1), len(text2))

def tag_frequent(weibo):
    tags = jieba.analyse.extract_tags(weibo)

    tag_freq = {}
    for tag in tags:
        tag_freq[tag] = 0

    segments = jieba.cut(weibo)
    for seg in segments:
#        print "Seg:", seg
        if seg in tag_freq:
            tag_freq[seg] += 1

#    for tag in tag_freq:
#        print "Freq: %s, %d" %(tag.encode(OUT_CODE), tag_freq[tag])
    return tag_freq
    
    
def euc_distance(text1, text2):
    text1_tag_freq = tag_frequent(text1) 
    text2_tag_freq = tag_frequent(text2)
    
    distance = .0
    for tag, freq in text1_tag_freq.items():
        if tag in text2_tag_freq:
            distance += math.pow((freq - text2_tag_freq[tag]), 2)
        else:
            distance += math.pow(freq, 2)

    for tag, freq in text2_tag_freq.items():
        if tag not in text1_tag_freq:
            distance += math.pow(freq, 2)
    
    return math.sqrt(distance)

def euc_similarity(text1, text2):
	ed = euc_distance(text1, text2)
	return 1 - ed / max(len(text1), len(text2))

def weibo_similarity(text1, text2, weight=0.5):
	lev_sim = lev_similarity(text1, text2)
	euc_sim = euc_similarity(text1, text2)
	return lev_sim * weight + (1 - weight) * euc_sim

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
