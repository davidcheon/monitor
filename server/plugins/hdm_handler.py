#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import base_path
from config import hosts
import threading
import time
class hdm_handler_thread(threading.Thread):
	def __init__(self,data,counter):
		threading.Thread.__init__(self)
		self.received_time=data['received_time']
		self.hdm_data_uswage=data['hdm']
		self.from_ip=data['from']
		self.host=hosts.hosts[self.from_ip]
		self.host_uswage_standards=self.host.servers['hdm']['uswage']
		self.counter=counter[self.from_ip]['hdm']
	def run(self):
		for device,uswage in self.hdm_data_uswage.items():
			self.counter[device].append(uswage)
			if len(self.counter[device])>10:
				self.counter[device]=self.counter[device][1:]
			if len(filter(lambda a:int(a[:-1])>self.host_uswage_standards['max'],self.counter[device]))>5:
				print '\033[42m <Hdm %s High Uswage > 5 times Warnings at %s >\033[0m \033[32m %s High_STANDARD:(%.2f%%) , NOW:(%.2f%%) \033[0m\n'%(device,time.ctime(self.received_time),self.from_ip,self.host_uswage_standards['max'],float(uswage[:-1]))
			


'''data=
{u'hdm': {u'/dev/shm': u'1%', u'/boot': u'18%', u'/media/\u6211\u7684\u5149\u76d8': u'100%', u'/': u'87%', u'/home': u'53%'}, 'received_time': 1442501366.021204, u'from': u'192.168.1.105', u'cpu': {u'idle': u'93.79', u'nice': u'0.00', u'system': u'2.18', u'user': u'3.27'}, u'memory': {u'mem_free': 23.0}}
			
		counter[h.ip]={'cpu':{
				'idle':[],			
				'nice':[],
				'system':[],
				'user':[],
				'received_time':[],
				},'memory':{
				'mem_free':[],
				},'hdm':{
				}
				}

'''
