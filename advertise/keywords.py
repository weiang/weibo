#! /usr/bin/env python
# -*- coding: utf-8 -*-

from snownlp import SnowNLP

weiboFd = open('text.txt', 'r')
keywordsFd = open('keywords.txt', 'w')

keywordsDict = {}
for line in weiboFd:
	line = line.decode(u'utf-8').strip(u'\n \t')
	s = SnowNLP(line)
	keywordsDict[line] = s.keywords(3)
	info = line
	for keyword in keywordsDict[line]:
		info += u' %s' % keyword
	info += u'\n'
	keywordsFd.write(info.encode(u'utf-8'))

weiboFd.close()
keywordsFd.close()
