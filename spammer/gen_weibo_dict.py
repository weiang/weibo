#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
	Usage: python ./gen_weibo_dict.py <data_set> [tag dict] [tag_pair dict]
		   Generate weibo tag dict and tag_pair dict.
'''

import math
import sys
import jieba
import jieba.analyse
import Levenshtein
from dictionary import *

IN_CODEC = u'utf-8'
OUT_CODEC = u'utf-8'

def usage():
	print __doc__

def weibo_tag_frequent(weibos):
	tag_frequent = {}
	for weibo in weibos:
		tags = jieba.analyse.extract_tags(weibo)
		for tag in tags:
			if tag not in tag_frequent:
				tag_frequent[tag] = 0
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
			result[tag] = float(adv_tag_frequent[tag] - normal_tag_frequent[tag]) / (adv_tag_frequent[tag] + normal_tag_frequent[tag])

	return result

def pair_tags(str1, str2):
	str1 = str1.strip(u' \n\t')
	str2 = str2.strip(u' \n\t')
# 	print 'key: %s, %s' %(str1.encode(OUT_CODEC), str2.encode(OUT_CODEC))

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
#				print '%d, %d' %(i, j)
				key = pair_tags(tags[i], tags[j])
#				print 'key: %s' %(key.encode(OUT_CODEC))
				if key not in weibo_tag_pair_frequent:
					weibo_tag_pair_frequent[key] = 0
				weibo_tag_pair_frequent[key] += 1
	
#	for tag_pair in weibo_tag_pair_frequent:
#		print '%s, %f' %(tag_pair.encode(OUT_CODEC), weibo_tag_pair_frequent[tag_pair])
	return weibo_tag_pair_frequent

def weibo_tag_pair_weight(advertisement_weibos, normal_weibos):
	adv_tag_pair_frequent = weibo_tag_pair_frequent(advertisement_weibos)
	normal_tag_pair_frequent = weibo_tag_pair_frequent(normal_weibos)

	result = {}
	for tag_pair in adv_tag_pair_frequent:
		if tag_pair not in normal_tag_pair_frequent:
			result[tag_pair] = 1.0
		else:
			result[tag_pair] = float(adv_tag_pair_frequent[tag_pair] - normal_tag_pair_frequent[tag_pair]) \
			/ (adv_tag_pair_frequent[tag_pair] + normal_tag_pair_frequent[tag_pair])

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
#        print "Freq: %s, %d" %(tag.encode(OUT_CODEC), tag_freq[tag])
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


def test_euc_similarity():
    text1 = u"全场 视频 包邮 颜色 现价 来自 小票 原价 推荐 专柜 情侣 示范 跑步 经典 亲们 时尚 促销 跑鞋"
    text2 = u"全场 全场 包邮 小票 原价 推荐 专柜 情侣 示范 跑步 经典 亲们 时尚 促销 跑鞋"
    
    dis = euc_distance(text1, text2)
    sim = euc_similarity(text1, text2)

    print "Dis: ", dis
    print "Sim: ", sim

def test_lev_similarity():
    text1 = u"全场 视频 包邮 颜色 现价 来自 小票 原价 推荐 专柜 情侣 示范 跑步 经典 亲们 时尚 促销 跑鞋"
    text2 = u"包邮 现价 来自 小票 原价 推荐 专柜 情侣 示范 跑步 经典 亲们 时尚 促销 跑鞋"

    dis = lev_distance(text1, text2)
    sim = lev_similarity(text1, text2)
    print "Dis: " ,dis
    print "Sim: ", sim

def test_weibo_similarity():
    text1 = u"全场 视频 包邮 颜色 现价 来自 小票 原价 推荐 专柜 情侣 示范 跑步 经典 亲们 时尚 促销 跑鞋"
    text2 = u"包邮 现价 来自 小票 原价 推荐 专柜 情侣 示范 跑步 经典 亲们 时尚 促销 跑鞋"

    print "weibo sim: ", weibo_similarity(text1, text2)
    
def get_weibo_dict(data_set, tag_dict, tag_pair_dict):
    advertisement_weibos = []
    normal_weibos = []
    fd = open(data_set, 'r')
    for line in fd:
	line = line.decode(IN_CODEC)
        line = line.strip(u' \t\n')
        flag, text = line.split(u'\t')
        if flag == u'1':
            advertisement_weibos.append(text)
        else:
            normal_weibos.append(text)
    fd.close()

    result = weibo_tag_weight(advertisement_weibos, normal_weibos)
    gen_tag_weight_dict(result, tag_dict)
    result = weibo_tag_pair_weight(advertisement_weibos, normal_weibos)
    gen_tag_pair_weight_dict(result, tag_pair_dict)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(-1)
    
    data_set = sys.argv[1]
    tag_dict = u'tag_weight.dict'
    tag_pair_dict = u'tag_pair_weight.dict'
    if len(sys.argv) >= 3:
        tag_dict = sys.argv[2]
    if len(sys.argv) >= 4:
        tag_pair_dict = sys.argv[3]

    get_weibo_dict(data_set, tag_dict, tag_pair_dict)

