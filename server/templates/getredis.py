#!/usr/bin/env python
#!_*_ coding:utf-8 _*_
import redis
from ConfigParser import ConfigParser
import os
def getredis():
	config=ConfigParser()
	config_file=os.path.join(os.path.dirname(os.path.dirname(__file__)),'config/config.py')
	config.read(config_file)
	r=redis.Redis(host=config.get('info','host'),password=config.get('info','password'))
	return r
