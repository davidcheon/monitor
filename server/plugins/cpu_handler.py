#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import base_path
from config import hosts
import threading
class cpu_handler_thread(threading.Thread):
	def __init__(self,data,from_ip,counter):
		threading.Thread.__init__(self)
		self.data=data['cpu']
		self.idle=float(self.data['idle'])
		self.nice=float(self.data['nice'])
		self.system=float(self.data['system'])
		self.user=float(self.data['user'])
		self.from_ip=from_ip
		self.received_time=int(data['received_time'])
		self.host_standards=hosts.hosts[self.from_ip].servers['cpu']
		self.idle_standards=self.host_standards['idle']
		
		self.nice_standards=self.host_standards['nice']
		self.system_standards=self.host_standards['system']
		self.user_standards=self.host_standards['user']
		self.interval=int(hosts.hosts[self.from_ip].interval)
		self.counter=counter
		
	def run(self):
		#print self.counter[self.from_ip]['cpu']
		self.counter[self.from_ip]['cpu']['idle'].append(self.idle)
		if len(self.counter[self.from_ip]['cpu']['idle'])>10:
			self.counter[self.from_ip]['cpu']['idle']=self.counter[self.from_ip]['cpu']['idle'][1:]
		self.counter[self.from_ip]['cpu']['nice'].append(self.nice)
		if len(self.counter[self.from_ip]['cpu']['nice'])>10:
			self.counter[self.from_ip]['cpu']['nice']=self.counter[self.from_ip]['cpu']['nice'][1:]
		self.counter[self.from_ip]['cpu']['system'].append(self.system)
		if len(self.counter[self.from_ip]['cpu']['system'])>10:
			self.counter[self.from_ip]['cpu']['system']=self.counter[self.from_ip]['cpu']['system'][1:]
		self.counter[self.from_ip]['cpu']['user'].append(self.user)
		if len(self.counter[self.from_ip]['cpu']['user'])>10:
			self.counter[self.from_ip]['cpu']['user']=self.counter[self.from_ip]['cpu']['user'][1:]
		self.counter[self.from_ip]['cpu']['received_time'].append(self.received_time)
		if len(self.counter[self.from_ip]['cpu']['received_time'])>10:
			self.counter[self.from_ip]['cpu']['received_time']=self.counter[self.from_ip]['cpu']['received_time'][1:]

		if len(self.counter[self.from_ip]['cpu']['received_time'])>1:
			minus_time=self.counter[self.from_ip]['cpu']['received_time'][-1]-self.counter[self.from_ip]['cpu']['received_time'][-2]
			if minus_time>self.interval+5:
				print '\033[43m <Connection TimeOut Warnings>\033[0m \033[33m From:%s ,Normal Interval:(%d) , NOW:(%d) \033[0m'%(self.from_ip,self.interval,minus_time)



		if len(filter(lambda a:a<float(self.idle_standards['min']),self.counter[self.from_ip]['cpu']['idle']))>5:
			print '\033[43m <Cpu Idle LowIdle > 5 times Warnings>\033[0m \033[33m %s LOW_IDLE:(%.2f) , NOW:(%.2f) \033[0m'%(self.from_ip,self.idle_standards['min'],self.idle)
		elif len(filter(lambda a:a>=float(self.idle_standards['max']),self.counter[self.from_ip]['cpu']['idle']))>5:
			print '\033[41m <Cpu Idle HighIdle > 5 times Warnings>\033[0m \033[31m %s HIGH_IDLE:(%.2f) , NOW:(%.2f) \033[0m'%(self.from_ip,self.idle_standards['max'],self.idle)
		if len(filter(lambda a:a<float(self.nice_standards['min']),self.counter[self.from_ip]['cpu']['nice']))>5:
			print '\033[43m <Cpu Nice HighPriority < 5 times Warnings>\033[0m \033[33m %s LOW_NICE:(%.2f) , NOW:(%.2f) \033[0m'%(self.from_ip,self.nice_standards['min'],self.nice)
		elif len(filter(lambda a:a>float(self.nice_standards['max']),self.counter[self.from_ip]['cpu']['nice']))>5:
			print '\033[41m <Cpu NICE LowPriority > 5 times Warnings>\033[0m \033[31m %s HIGH_NICE:(%.2f) , NOW:(%.2f) \033[0m'%(self.from_ip,self.idle_standards['max'],self.idle)
		if len(filter(lambda a:a<float(self.system_standards['min']),self.counter[self.from_ip]['cpu']['system']))>5:
			print '\033[43m <Cpu System LowSystemUse > 5 times Warnings>\033[0m \033[33m %s LOW_SYSTEM:(%.2f) , NOW:(%.2f) \033[0m'%(self.from_ip,self.system_standards['min'],self.system)
		elif len(filter(lambda a:a>float(self.system_standards['max']),self.counter[self.from_ip]['cpu']['system']))>5:
			print '\033[41m <Cpu System HighSystemUse > 5 times Warnings>\033[0m \033[31m %s HIGH_SYSTEM:(%.2f) , NOW:(%.2f) \033[0m'%(self.from_ip,self.system_standards['max'],self.system)
		if len(filter(lambda a:a<float(self.user_standards['min']),self.counter[self.from_ip]['cpu']['user']))>5:
			print '\033[43m <Cpu User LowUserUse > 5 times Warnings>\033[0m \033[33m %s LOW_USER:(%.2f) , NOW:(%.2f) \033[0m'%(self.from_ip,self.user_standards['min'],self.user)
		elif len(filter(lambda a:a>float(self.user_standards['max']),self.counter[self.from_ip]['cpu']['user']))>5:
			print '\033[41m <Cpu User HighUser > 5 times Warnings>\033[0m \033[31m %s HIGH_USER:(%.2f) , NOW:(%.2f) \033[0m'%(self.from_ip,self.user_standards['max'],self.user)
'''
 {u'idle': u'93.79', u'nice': u'0.00', u'system': u'2.18', u'user': u'3.27'}
'''
