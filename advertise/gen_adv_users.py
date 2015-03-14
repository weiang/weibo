#! /usr/bin/env python
# -*- encoding: utf-8 -*-

'''
	Usage: python ./gen_adv_users.py <user weibo file> <weibos> <predict result>
		   Genrate test weibo set from user's weibo list
		   <user weibo file>: <uid>\t<weibo 1>\t<weibo 2>...\t...\t<weibo n>
		   <weibos>: 0\t<weibo>
		   <predict result>: 1 if is adv, else 0 
'''

import os
import sys
import json
import codecs
from global_config import *

IN_CODEC = u'utf-8'
OUT_CODEC = u'utf-8'

global_config = Global_config()

def is_advertisor(rate):
	if rate >= global_config.advertiser_threshold:
		return True
	else:
		return False

if __name__ == u'__main__':
	if len(sys.argv) < 4:
		print __doc__
		sys.exit(-1)

	userfd = codecs.open(sys.argv[1], u'r', IN_CODEC)
	weibofd = codecs.open(sys.argv[2], u'r', IN_CODEC)
	prefd = codecs.open(sys.argv[3], u'r', IN_CODEC)

	# User
	users = {}
	for line in userfd:
		ls = line.strip(u' \t\n').split(u'\t')
		uid = ls[0]
		weibos = ls[1:]
		users[uid] = []
		for weibo in weibos:
			users[uid].append(weibo)


	# Weibo
	weibos = []
	for line in weibofd:
		flag, weibo = line.strip(u' \t\n').split(u'\t')
		weibos.append(weibo)

	pre = []
	for line in prefd:
		pre.append(int(line.strip(u' \t\n')))

	weibo_pre = dict(zip(weibos, pre))
    
#        for w in weibo_pre:
#            print w, weibo_pre[w]
	user_ad_counts = {}
	for user in users:
		user_ad_counts[user] = 0
		for weibo in users[user]:
		    user_ad_counts[user] += weibo_pre[weibo]
		total_weibos = len(users[user])
		ad_rate = float(user_ad_counts[user]) / total_weibos
		if is_advertisor(ad_rate):
			print user

	userfd.close()
	weibofd.close()
	prefd.close()
