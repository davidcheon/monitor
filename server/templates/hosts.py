#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import base_path
from templates import base_templates
import redis
import json
import threading
class host:
	def __init__(self,ip):
		self.ip=ip
		self.servers={'cpu':base_templates.cpu().params,
				'memory':base_templates.memory().params,
				'hdm':base_templates.hdm().params}
class mythread(threading.Thread):
	def __init__(self,recv_data):
		threading.Thread.__init__(self)
		self.recv_data=recv_data
	def run(self):
		cpu_data=self.recv_data['cpu']
		memory_data=self.recv_data['memory']
		hdm_data=self.recv_data['hdm']
		print cpu_data,memory_data,hdm_data
if __name__=='__main__':
	r=redis.Redis(host='127.0.0.1',password='daisongchen')
	ps=r.pubsub()
	hosts=[host('192.168.0.200'),host('192.168.0.132')]
	chanels=[]
	if r.ping():
		for h in hosts:
			chanel='chanel:%s'%h.ip
			chanels.append(chanel)
			h.servers['channel']=chanel
			r.set(h.ip,json.dumps(h.servers))
		ps.subscribe(chanels)
		for n in xrange(len(chanels)):
			ps.parse_response()
		#for item in ps.listen():
		#	if item['type']=='message':
		#		t=mythread(json.loads(item['data']))
		#		t.start()
		while 1:
			recv_data=ps.parse_response()	
			print recv_data
			t=mythread(json.loads(recv_data[2]))
			t.start()
	else:
		print 'redis connect failed'








