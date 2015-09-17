#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import base_path
from templates import host
from ConfigParser import ConfigParser
import os
'''
class host:
	def __init__(self,ip,interval):
		self.ip=ip
		self.servers={'cpu':base_templates.cpu().params,
				'memory':base_templates.memory().params,
				'hdm':base_templates.hdm().params,
				}
		self.interval=interval
'''
config=ConfigParser()
config_file=os.path.join(os.path.dirname(os.path.dirname(__file__)),'config/config.py')
config.read(config_file)
hosts=[]
interval=config.get('interval','value')
for ip in config.items('clients'):
	hosts.append(host.host(ip[1],interval))
channels=[]
for channel in config.items('channels'):
	channels.append(channel[1])
	


