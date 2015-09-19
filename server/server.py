#!/usr/bin/python
#!_*_ coding:utf-8 _*_
#from templates import base_path
from templates import base_templates
from templates import getredis as red
from plugins import cpu_handler,memory_handler,hdm_handler
from config import hosts as hs
import json
import threading
import sys
import random
import signal
import time
class host:
	def __init__(self,ip):
		self.ip=ip
		self.servers={'cpu':base_templates.cpu().params,
				'memory':base_templates.memory().params,
				'hdm':base_templates.hdm().params}
class mythread(threading.Thread):
	def __init__(self,recv_data,counter):
		threading.Thread.__init__(self)
		self.recv_data=recv_data['data']
		self.from_ip=self.recv_data['from']
		self.counter=counter
	def run(self):
		try:
			self.recv_data['received_time']=time.time()
			threads=[]
			t_cpu=cpu_handler.cpu_handler_thread(self.recv_data,self.counter)	
			t_memory=memory_handler.memory_handler_thread(self.recv_data,self.counter)
			t_hdm=hdm_handler.hdm_handler_thread(self.recv_data,self.counter)
			threads.append(t_cpu)
			threads.append(t_memory)
			threads.append(t_hdm)
			t_cpu.start()
			t_memory.start()
			t_hdm.start()
			for t in threads:
				t.join()
 			'''self.recv_data=
{u'hdm': {u'/dev/shm': u'1%', u'/boot': u'18%', u'/media/\u6211\u7684\u5149\u76d8': u'100%', u'/': u'87%', u'/home': u'53%'}, 'received_time': 1442501366.021204, u'from': u'192.168.1.105', u'cpu': {u'idle': u'93.79', u'nice': u'0.00', u'system': u'2.18', u'user': u'3.27'}, u'memory': {u'mem_free': 23.0}}
			'''

		except TypeError,e:
			print '%s send type error'%self.from_ip,e
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
	try:
		r.ping()
	except Exception,e:
		print e
	else:
		ps=r.pubsub()
		hosts=hs.hosts
		channels=hs.channels
		counter={}
		for h in hosts.values():
			send_data={}
			channel=random.choice(hs.channels)
			send_data['channel']=channel
			temp_servers={}
			for server in h.servers.keys():
				temp_servers[server]=server+'_info'
			send_data['servers']=temp_servers
			send_data['interval']=h.interval
			send_data['cpu_interval']=h.servers['cpu']['cpu_interval']
			r.set(h.ip,json.dumps(send_data))
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
		ps.subscribe(channels)
		#for item in ps.listen():
		#	if item['type']=='message':
		#		t=mythread(json.loads(item['data']))
		#		t.start()
		for n in xrange(len(channels)):
			ps.parse_response()
		host_hdm_status={}
		for host in hs.hosts.values():
			host_hdm_status[str(host.ip)]=False
		while 1:
			recv_data=ps.parse_response()[2]
			recv_data=json.loads(recv_data)
			from_ip=recv_data['data']['from']
			if not host_hdm_status[from_ip]:
				for device in recv_data['data']['hdm'].keys():
						counter[from_ip]['hdm'][device]=[]
				
			host_hdm_status[from_ip]=True
			t=mythread(recv_data,counter)
			t.start()








