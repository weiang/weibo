#!/usr/bin/env python
# -*- encoding=utf-8 -*-

# Global configuration

class Singleton(object):
	def __new__(cls, *args, **kw):
		if not hasattr(cls, '_instance'):
			orig = super(Singleton, cls)
			cls._instance = orig.__new__(cls, *args, **kw)
		return cls._instance

class Global_config(Singleton):
    advertiser_threshold = 0.5
    advertisement_frequent_tags = 5
    advertisement_frequent_tags_pair = 5
