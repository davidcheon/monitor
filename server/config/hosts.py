#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import base_path
from templates import host
from ConfigParser import ConfigParser
import os

config=ConfigParser()
config_file=os.path.join(os.path.dirname(os.path.dirname(__file__)),'config/config.py')
config.read(config_file)
hosts={}
interval=config.get('interval','value')
for ip in config.items('clients'):
	hosts[ip[1]]=host.host(ip[1],interval)
channels=[]
for channel in config.items('channels'):
	channels.append(channel[1])
	


