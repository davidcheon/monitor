#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import base_path
from config import hosts
import threading
import time
class cpu_handler_thread(threading.Thread):
	def __init__(self,data,counter):
		threading.Thread.__init__(self)
		self.data=data['cpu']
		self.idle=float(self.data['idle'])
		self.nice=float(self.data['nice'])
		self.system=float(self.data['system'])
		self.user=float(self.data['user'])
		self.from_ip=data['from']
		self.received_time=int(data['received_time'])
		self.host_standards=hosts.hosts[self.from_ip].servers['cpu']
		self.idle_standards=self.host_standards['idle']
		
		self.nice_standards=self.host_standards['nice']
		self.system_standards=self.host_standards['system']
		self.user_standards=self.host_standards['user']
		self.interval=int(hosts.hosts[self.from_ip].interval)
		self.counter=counter[self.from_ip]['cpu']
		self.received_time=data['received_time']
	def run(self):
		#print self.counter[self.from_ip]['cpu']
		self.counter['idle'].append(self.idle)
		if len(self.counter['idle'])>10:
			self.counter['idle']=self.counter['idle'][1:]
		self.counter['nice'].append(self.nice)
		if len(self.counter['nice'])>10:
			self.counter['nice']=self.counter['nice'][1:]
		self.counter['system'].append(self.system)
		if len(self.counter['system'])>10:
			self.counter['system']=self.counter['system'][1:]
		self.counter['user'].append(self.user)
		if len(self.counter['user'])>10:
			self.counter['user']=self.counter['user'][1:]
		self.counter['received_time'].append(self.received_time)
		if len(self.counter['received_time'])>10:
			self.counter['received_time']=self.counter['received_time'][1:]

		if len(self.counter['received_time'])>1:
			minus_time=self.counter['received_time'][-1]-self.counter['received_time'][-2]
			if minus_time>self.interval+5:
				print '\033[43m <Connection TimeOut Warnings at %s >\033[0m \033[33m From:%s ,Normal Interval:(%d) , NOW:(%d) \033[0m'%(time.ctime(self.received_time),self.from_ip,self.interval,minus_time)



		if len(filter(lambda a:a<float(self.idle_standards['min']),self.counter['idle']))>5:
			print '\033[43m <Cpu Idle LowIdle  > 5 times Warnings at %s >\033[0m \033[33m %s LOW_IDLE:(%.2f) , NOW:(%.2f) \033[0m'%(time.ctime(self.received_time),self.from_ip,self.idle_standards['min'],self.idle)
		elif len(filter(lambda a:a>=float(self.idle_standards['max']),self.counter['idle']))>5:
			print '\033[41m <Cpu Idle HighIdle  > 5 times Warnings at %s >\033[0m \033[31m %s HIGH_IDLE:(%.2f) , NOW:(%.2f) \033[0m'%(time.ctime(self.received_time),self.from_ip,self.idle_standards['max'],self.idle)
		if len(filter(lambda a:a<float(self.nice_standards['min']),self.counter['nice']))>5:
			print '\033[43m <Cpu Nice HighPriority < 5 times Warnings at %s >\033[0m \033[33m %s LOW_NICE:(%.2f) , NOW:(%.2f) \033[0m'%(time.ctime(self.received_time),self.from_ip,self.nice_standards['min'],self.nice)
		elif len(filter(lambda a:a>float(self.nice_standards['max']),self.counter['nice']))>5:
			print '\033[41m <Cpu NICE LowPriority > 5 times Warnings at %s >\033[0m \033[31m %s HIGH_NICE:(%.2f) , NOW:(%.2f) \033[0m'%(time.ctime(self.received_time),self.from_ip,self.idle_standards['max'],self.idle)
		if len(filter(lambda a:a<float(self.system_standards['min']),self.counter['system']))>5:
			print '\033[43m <Cpu System LowSystemUse > 5 times Warnings at %s >\033[0m \033[33m %s LOW_SYSTEM:(%.2f) , NOW:(%.2f) \033[0m'%(time.ctime(self.received_time),self.from_ip,self.system_standards['min'],self.system)
		elif len(filter(lambda a:a>float(self.system_standards['max']),self.counter['system']))>5:
			print '\033[41m <Cpu System HighSystemUse > 5 times Warnings at %s >\033[0m \033[31m %s HIGH_SYSTEM:(%.2f) , NOW:(%.2f) \033[0m'%(time.ctime(self.received_time),self.from_ip,self.system_standards['max'],self.system)
		if len(filter(lambda a:a<float(self.user_standards['min']),self.counter['user']))>5:
			print '\033[43m <Cpu User LowUserUse > 5 times Warnings at %s >\033[0m \033[33m %s LOW_USER:(%.2f) , NOW:(%.2f) \033[0m'%(time.ctime(self.received_time),self.from_ip,self.user_standards['min'],self.user)
		elif len(filter(lambda a:a>float(self.user_standards['max']),self.counter['user']))>5:
			print '\033[41m <Cpu User HighUser > 5 times Warnings at %s >\033[0m \033[31m %s HIGH_USER:(%.2f) , NOW:(%.2f) \033[0m'%(time.ctime(self.received_time),self.from_ip,self.user_standards['max'],self.user)
'''
 {u'idle': u'93.79', u'nice': u'0.00', u'system': u'2.18', u'user': u'3.27'}
'''

