#!/usr/bin/python
#!_*_ coding:utf-8 _*_
#from templates import base_path
from templates import base_templates
from templates import getredis as red
from config import hosts as hs
import json
import threading
import sys
import random
import signal
class host:
	def __init__(self,ip):
		self.ip=ip
		self.servers={'cpu':base_templates.cpu().params,
				'memory':base_templates.memory().params,
				'hdm':base_templates.hdm().params}
class mythread(threading.Thread):
	def __init__(self,recv_data):
		threading.Thread.__init__(self)
		self.recv_data=recv_data['data']
		self.from_ip=self.recv_data['from']
	def run(self):
		try:
			cpu_data=self.recv_data['cpu']
			memory_data=self.recv_data['memory']
			hdm_data=self.recv_data['hdm']
			print cpu_data,memory_data,hdm_data
		except TypeError,e:
			print '%s send type error'%self.from_ip
		except KeyError,e:
			print '%s send keyerror'%self.from_ip
def handler(signum,frame):
	global r
	r.flushall()
	#r.shutdown()
	sys.exit(0)
if __name__=='__main__':
	signal.signal(signal.SIGINT,handler)
	signal.signal(signal.SIGTERM,handler)
	r=red.getredis()
	if r.ping():
		ps=r.pubsub()
		hosts=hs.hosts
		channels=hs.channels
		for h in hosts:
			send_data={}
			channel=random.choice(hs.channels)
			send_data['channel']=channel
			temp_servers={}
			for server in h.servers.keys():
				temp_servers[server]=server+'_info'
			send_data['servers']=temp_servers
			send_data['interval']=h.interval
			r.set(h.ip,json.dumps(send_data))
		ps.subscribe(channels)
		#for item in ps.listen():
		#	if item['type']=='message':
		#		t=mythread(json.loads(item['data']))
		#		t.start()
		for n in xrange(len(channels)):
			ps.parse_response()
		while 1:
			recv_data=ps.parse_response()	
			t=mythread(json.loads(recv_data[2]))
			t.start()
	else:
		print 'redis connect failed'








