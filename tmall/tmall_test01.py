#!/usr/bin/env python
# encoding: utf-8

import urllib2
from pyquery import PyQuery as pq
import Queue
import json
import threading
import sys
import time
import os
import datetime
import urllib
import socket
## 这段代码是用于解决中文报错的问题 
reload(sys) 
sys.setdefaultencoding("utf8") 
#####################################################
# url = "http://store.taobao.com/search.htm?user_number_id=" + str(id) +"&orderType=hotsell_desc"
detail = []
file_tmall = open('tmall.txt','w+')
url = "http://store.taobao.com/search.htm?user_number_id=1749873883&orderType=hotsell_desc"
header = {
	"Cookie":"v=0; cookie2=19ab901ab5cdd9a784603f10fa654e85; t=1eda35588634d73414728baa52949a8d; cna=n9XhDMLuIUMCAbaXcc7prlDO; uc1=cookie14=UoW29b2XbEq6wg%3D%3D; isg=75232DA1FA0F8E1D5BD6E33560AAB308; _tb_token_=gsiLkDrQe8aa",
	"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36"
}
req = urllib2.Request(url,None,header)
response = urllib2.urlopen(req,timeout = 5)
result = response.read()

doc = pq(result)

length_res = doc("b[class = 'ui-page-s-len']").text()
start = length_res.find("/")
length = length_res[start+1:]
while True:
	try:

		for i in range(1,int(length)+1):
			url_get = "http://store.taobao.com/search.htm?user_number_id=1749873883&orderType=hotsell_desc&pageNo=" + str(i)
			req_get = urllib2.Request(url_get,None,header)
			response_get = urllib2.urlopen(req_get,timeout = 5)
			result_get = response_get.read()

			doc_get = pq(result_get)

			length_get = len(doc_get("div[class = 'J_TItems']").find("dl"))
			# print length_get
			for j in range(length_get-10):
				title =  doc_get("div[class = 'J_TItems']").find("dl").eq(j)(".detail").find("a").text()
				price = doc_get("div[class = 'J_TItems']").find("dl").eq(j)(".detail")(".c-price").text()
				if doc_get("div[class = 'J_TItems']").find("dl").eq(j)(".detail")(".sale-num"):
					salenum = doc_get("div[class = 'J_TItems']").find("dl").eq(j)(".detail")(".sale-num").text()
				else :
					salenum = -1
				if  doc_get("div[class = 'J_TItems']").find("dl").eq(j)(".rates").find("span"):
					comments = doc_get("div[class = 'J_TItems']").find("dl").eq(j)(".rates").find("span").text()
					start_com = comments.find(": ")
					comments = comments[start_com+1:]
				else:
					comments = -1

				print str(title) +"\t" + str(price )+ "\t" + str(salenum) +"\t" + str(comments)
				each_detail = {
					"title" : title,
					"price" : price,
					"salenum" : salenum,
					"commentsNum" : comments
				}
				detail.append(each_detail)
		break
	except Exception,e:
		print e

record = {
	"urlId":"urlId",
	"detail" : detail
}
json_record = json.loads(json.dumps(record))
# mutex.acquire()
file_tmall.write(json.dumps(json_record, ensure_ascii=False) + "\n")
print "1"
file_tmall.flush()
# mutex.release()