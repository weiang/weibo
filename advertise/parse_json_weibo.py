#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import json
import codecs

IN_CODEC = u'utf-8'
OUT_CODEC = u'utf-8'

global_user_weibos = {}

def get_user_weibos(path):
	fd = codecs.open(path, u'r')

	for line in fd:
		objects = json.loads(line)
		for user_info in objects:
			if u'userId' in user_info:
				uid = user_info[u'userId']
				if uid not in global_user_weibos:
					global_user_weibos[uid] = []
				content = user_info[u'content']
				global_user_weibos[uid].append(content)

def output(result, outfile=sys.stdout):
	for key, values in result.items():
		info = u'%s' %(key)
		for value in values:
			info += u'\t%s' %(value)
		info += u'\n'
		outfile.write(info)

if __name__ == u'__main__':
	if len(sys.argv) < 2:
		print 'Usage: %s <data dir> [out file]' %(sys.argv[0])
		sys.exit(-1)

	dirname = sys.argv[1]

	for path in os.listdir(dirname):
		if not os.path.isdir(path):
#			print "Path: ", path
			get_user_weibos(dirname + u'/' + path)

	if len(sys.argv) >= 3:
		fd = codecs.open(sys.argv[2], u'w', OUT_CODEC)
	else:
		fd = sys.stdout

	output(global_user_weibos, fd)

	if len(sys.argv) >= 3:
		fd.close()