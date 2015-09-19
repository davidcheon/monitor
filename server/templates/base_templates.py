#!/usr/bin/python
#!_*_ coding:utf-8 _*_
class cpu:
	def __init__(self):
		self.server_name='cpu_server'
		self.params={'user':{'min':0,'max':50},
			     'nice':{'min':0,'max':5},
			     'system':{'min':0,'max':30},
			     'idle':{'min':0,'max':10},
			     'cpu_interval':3}
class memory:
	def __init__(self):
		self.server_name='memory_server'
		self.params={'mem_free':{'min':50,'max':70}
			     
			}

class hdm:
	def __init__(self):
		self.server_name='hdm_server'
		#self.params={'home_use':{'min':0,'max':90},
		#	     'boot_use':{'min':0,'max':90},
		#	     'root_use':{'min':0,'max':90},
		#	     'usr_use':{'min':0,'max':90}
		#}
		self.params={'uswage':{'min':10,'max':80}}

