#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import base_templates
class host:
	def __init__(self,ip,interval):
		self.ip=ip
		self.servers={'cpu':base_templates.cpu().params,
				'memory':base_templates.memory().params,
				'hdm':base_templates.hdm().params,
				}
		self.interval=interval
