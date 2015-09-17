#!/usr/bin/python
#!_*_ coding:utf-8 _*_
class MyException(Exception):
	def __init__(self,data):
		Exception.__init__(self)
		self.data=data
