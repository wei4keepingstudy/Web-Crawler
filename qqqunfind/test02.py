# -*- coding=utf-8 -*-
# Created Time: Mon 11 Aug 2014 11:45:25 AM CST
# File Name: single.py

import requests
import cgitb
import traceback
import sys
import hashlib
from pyquery import PyQuery as py
import time
import json
import re
import threading
import Queue
## 这段代码是用于解决中文报错的问题 
reload(sys) 
sys.setdefaultencoding("utf8") 
#####################################################


def main():
	# qqlogin_id = open("qqlogin.txt","r")#2
	sfile = open('qunidtest.txt', 'r')#9
	count = 1
	while count:
		qqlogin_id = open("qqlogin.txt","r")#2
		for username in qqlogin_id:
			count += 1
			username = username[0:9]
			print username
			passwd = 'q335q6123'		
			
			qq_list = []
			for i in range(3):
				lines = sfile.readline()
				if not lines:
					count =0

				print "1"
				print "line~~~~~~" + str(lines)

			# break
		if not lines:
			break
		# if count ==2:



if __name__ == '__main__':
	main()