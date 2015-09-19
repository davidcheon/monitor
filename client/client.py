#!/usr/bin/env python
#!_*_ coding:utf-8 _*_
from templates import getredis,getip,MyException
from plugins import cpu,hdm,memory
from ConfigParser import ConfigParser
import json
import time
import threading
import signal
import sys
class client:
	def __init__(self,redis,ip):
		self.redis=redis
		self.status=False or self.redis.ping()
		self.can_start_plugins=False
		self.local_ip=ip
	def start(self):
		if self.status:
			val=self.redis.get(self.local_ip)
			if  val:
				self.val=json.loads(val)
				self.channel=self.val['channel']
				self.interval=int(self.val['interval'])
				self.servers=self.val['servers']
				self.cpu_interval=self.val['cpu_interval']
				self.can_start_plugins=True
				self.start_plugins()
			else:
				print 'no data load'
		else:
			print 'redis connection failed'

	def start_plugins(self):
		if self.can_start_plugins:
			while 1:
				self.threads=[]
				completed_values={'from':self.local_ip}
				try:
					for servername,func in self.servers.items():
						try:
							t=my_exe_func_thread(servername,func,completed_values)
							self.threads.append(t)
							t.start()
						except Exception,e:
							print '\033[31m %s execute %s() failed \033[0m'%(servername,func)
				except MyException.MyException,e:
					print e.data
				finally:
					for t in self.threads:
						t.join()
					#time.sleep(self.interval)
					if self.interval>self.cpu_interval:
						time.sleep(self.interval-self.cpu_interval)
					t=send_data_thread(completed_values,self.channel,self.redis)
					t.start()
					t.join()
		else:
			print 'can not start plugins func'
class my_exe_func_thread(threading.Thread):
	def __init__(self,servername,func,completed_values):
		threading.Thread.__init__(self)
		self.completed_values=completed_values
		self.servername=servername
		self.func=func
	def run(self):
		func_ref=getattr(eval(self.servername),self.func)
		try:
			data=func_ref()
			self.completed_values[self.servername]=data
		except MyException.MyException,e:
			print '\033[31m Error:%s  \033[0m'%e.data
class send_data_thread(threading.Thread):
	def __init__(self,data,channel,redis):
		threading.Thread.__init__(self)
		self.data=data
		self.channel=channel
		self.redis=redis
	def run(self):
		self.redis.publish(self.channel,json.dumps({'data':self.data}))
def exit_handler(signum,frame):
	global red
	global ip
	for item in red.client_list():
		if item['addr'].startswith(ip):
			red.client_kill(item['addr'])
	sys.exit(0)
if __name__=='__main__':
	signal.signal(signal.SIGINT,exit_handler)
	signal.signal(signal.SIGTERM,exit_handler)
	red=getredis.getredis()
	config=ConfigParser()
	config.read('config/config.py')
	interface=config.get('extra','interface')
	ip=getip.get_ip_address(interface)
	cli=client(red,ip)
	cli.start()
	
