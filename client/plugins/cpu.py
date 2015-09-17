#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import base_path
from templates import MyException
import commands
def cpu_info():
	cmd='sar 1 3| grep -i average|awk \'{printf "%.2f\t%.2f\t%.2f\t%.2f",$3,$4,$5,$8}\''
	result=commands.getstatusoutput(cmd)
	if not result[0]:
		user,nice,system,idle=result[1].split()
		return {'user':user,
			'nice':nice,
			'system':system,
			'idle':idle}		
	else:
		raise MyException.MyException('cpu command failed')
'''
{'system': '1.85', 'idle': '90.67', 'user': '4.62', 'nice': '0.00'}
'''
