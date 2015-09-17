#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import base_path
from templates import MyException
import commands
import re
def hdm_info():
	cmd='df -h | grep  -v -i filesystem'
	status,result=commands.getstatusoutput(cmd)
	if not status:
		pat=re.compile('(\d+%)\s*(.*)')
		rs=pat.findall(result)
		d={}
		for v in rs:
			d[v[1]]=v[0]
		return d
	else:
		raise MyException.MyException('hdm command failed')
'''
{'/media/\xe6\x88\x91\xe7\x9a\x84\xe5\x85\x89\xe7\x9b\x98': '100%', '/boot': '18%', '/home': '53%', '/': '87%', '/dev/shm': '1%'}
'''
