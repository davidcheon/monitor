#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import base_path
from config import hosts
import threading
import time
class memory_handler_thread(threading.Thread):
	def __init__(self,data,counter):
		threading.Thread.__init__(self)
		self.data=data['memory']
		self.mem_free=float(self.data['mem_free'])
		self.from_ip=data['from']
		self.counter=counter[self.from_ip]['memory']
		self.hosts_standards=hosts.hosts[self.from_ip]
		self.host_server=self.hosts_standards.servers['memory']
		self.mem_free_standards=self.host_server['mem_free']
		self.received_time=data['received_time']
	def run(self):
		
		self.counter['mem_free'].append(self.mem_free)
		if len(self.counter['mem_free'])>10:
			self.counter['mem_free']=self.counter['mem_free'][1:]
		
		if len(filter(lambda a:a<self.mem_free_standards['min'],self.counter['mem_free']))>5:
			print '\033[44m <Memory LowFree  > 5 times Warnings at %s >\033[0m \033[34m %s LOW_STANDARD:(%.2f) , NOW:(%.2f) \033[0m'%(time.ctime(self.received_time),self.from_ip,self.mem_free_standards['min'],self.mem_free)
		elif len(filter(lambda a:a>=self.mem_free_standards['max'],self.counter['mem_free']))>5:
			print '\033[46m <Memory HighFree  > 5 times Warnings at %s >\033[0m \033[36m %s HIGHT_STANDARD:(%.2f) , NOW:(%.2f) \033[0m'%(time.ctime(self.received_time),self.from_ip,self.mem_free_standards['max'],self.mem_free)

'''data=
{u'hdm': {u'/dev/shm': u'1%', u'/boot': u'18%', u'/media/\u6211\u7684\u5149\u76d8': u'100%', u'/': u'87%', u'/home': u'53%'}, 'received_time': 1442501366.021204, u'from': u'192.168.1.105', u'cpu': {u'idle': u'93.79', u'nice': u'0.00', u'system': u'2.18', u'user': u'3.27'}, u'memory': {u'mem_free': 23.0}}
'''
