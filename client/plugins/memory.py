#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import base_path
from templates import MyException
import commands
def memory_info():
	cmd='free -m | grep -i mem|awk \'{printf"%d\t%d",$2,$4}\''
	status,result=commands.getstatusoutput(cmd)
	if not status:
		total,free=result.split()
		num='%.2f'%(float(free)/float(total))
		
		return {'mem_free':float(num)*100}
	else:
		raise MyException.MyException('memory command failed')
'''
{'mem_free': 49.0}
'''
