#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import socket
import fcntl
import struct
def get_ip_address(name):
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
	s.fileno(),
	0x8915,
	struct.pack('256s',name[:15])
	)[20:24])
