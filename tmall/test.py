#!/usr/bin/env python
# encoding: utf-8

import urllib2
from pyquery import PyQuery as pq
import Queue
import json
import threading
import sys
import time
import requests
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
url = "http://store.taobao.com/search.htm?user_number_id=1069174418&orderType=hotsell_des"
# url = "http://store.taobao.com/search.htm?user_number_id=733123801&orderType=hotsell_desc"
s = requests.Session()
header = {
	# "Cookie":"cna=R7z0DDTLsD8CAavZn79iYZJV; _tb_token_=Z5dYVQzfOApw; uc3=nk2=AGiWgxFL6CXP&id2=UojWl%2FVCPxHp1A%3D%3D&vt3=F8dATSsNRP5MusMpXtY%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D; lgc=crazyvgod; tracknick=crazyvgod; cookie2=d66683555f5237171f91367425374511; cookie1=Vv7MWfE6kqez2IW8DOtp8AwI9SYxJxc04%2FbymvAYyo4%3D; unb=1922391426; t=84406d0ab1710cc1f328aca8b7c410e8; _l_g_=Ug%3D%3D; _nk_=crazyvgod; cookie17=UojWl%2FVCPxHp1A%3D%3D; uc1=cookie15=W5iHLLyFOGW7aA%3D%3D&existShop=false; login=true; pnm_cku822=; isg=38659548C1DC9AC553745FAA3693B000; cq=ccp%3D0; CNZZDATA1000279581=881858599-1416477420-%7C1416477420; swfstore=288100; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; whl=-1%260%260%260; x=__ll%3D-1%26_ato%3D0",
	"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36"
}
# response = s.get(
# 	url,
# 	headers = header
# 	)
# result = response.text
# if "店铺浏览-淘宝网" not in result:
# 	if "J_TCrumbSearchForm" not in  result and "J_UserSearchParams"  not in result:
# 		if "jp_item" not in result:
# 			print "IP has been killed!!!!!!!!!"
# 			# continue
# 		else:
# 			pass
# 	else:
# 		doc = pq(result)
# 		if doc("b[class = 'ui-page-s-len']"):

# 			length_res = doc("b[class = 'ui-page-s-len']").text()
# 			print length_res
# 			start = length_res.find("/")
# 			length = length_res[start+1:]

# 			# self.get_result(urlId,length)
# 		elif doc("span[class =  'page-info']"):
# 			length_res = doc("span[class =  'page-info']").text()
# 			start = length_res.find("/")
# 			length = length_res[start+1:]
# 			# self.get_result(urlId,length)
# 		else:
# 			length = 0
# 			# self.get_result(urlId,length)

# else:
# 	length = 0
	# self.get_result(urlId,length)		
# req = urllib2.Request(url,None,header)
# response = urllib2.urlopen(req,timeout = 5)
# result = response.read()
response = s.get(
	url,
	headers = header
	)
result = response.text
# if "J_TCrumbSearchForm" not in result:
# 	print "IP has been killed!!!!!!!!!"
# 	# continue
# else:
# 	doc = pq(result)
# 	if doc("b[class = 'ui-page-s-len']"):

# 		length_res = doc("b[class = 'ui-page-s-len']").text()
# 		print length_res
# print result
doc = pq(result)

length_res = doc("b[class = 'ui-page-s-len']").text()
print length_res
# start = length_res.find("/")
# length = length_res[start+1:]
# while True:
# 	try:

# 		for i in range(1,int(length)+1):
# 			url_get = "http://store.taobao.com/search.htm?user_number_id=733123801&orderType=hotsell_desc&pageNo=" + str(i)
# 			# req_get = urllib2.Request(url_get,None,header)
# 			# response_get = urllib2.urlopen(req_get,timeout = 5)
# 			# result_get = response_get.read()
# 			response = s.get(
# 				url_get,
# 				headers = header
# 				)
# 			result_get = response.read()

# 			doc_get = pq(result_get)

# 			length_get = len(doc_get("div[class = 'J_TItems']").find("dl"))
# 			print length_get
# 			for j in range(length_get-10):
# 				title =  doc_get("div[class = 'J_TItems']").find("dl").eq(j)(".detail").find("a").text()
# 				price = doc_get("div[class = 'J_TItems']").find("dl").eq(j)(".detail")(".c-price").text()
# 				if doc_get("div[class = 'J_TItems']").find("dl").eq(j)(".detail")(".sale-num"):
# 					salenum = doc_get("div[class = 'J_TItems']").find("dl").eq(j)(".detail")(".sale-num").text()
# 				else :
# 					salenum = -1
# 				if  doc_get("div[class = 'J_TItems']").find("dl").eq(j)(".rates").find("span"):
# 					comments = doc_get("div[class = 'J_TItems']").find("dl").eq(j)(".rates").find("span").text()
# 					start_com = comments.find(": ")
# 					comments = comments[start_com+1:]
# 				else:
# 					comments = -1

# 				# print str(title) +"\t" + str(price )+ "\t" + str(salenum) +"\t" + str(comments)
# 				each_detail = {
# 					"title" : title,
# 					"price" : price,
# 					"salenum" : salenum,
# 					"commentsNum" : comments
# 				}
# 				detail.append(each_detail)
# 		break
# 	except Exception,e:
# 		print e

# record = {
# 	"urlId":urlId,
# 	"detail" : detail
# }
# json_record = json.loads(json.dumps(record))
# # mutex.acquire()
# file_tmall.write(json.dumps(json_record, ensure_ascii=False) + "\n")
# print "1"
# file_tmall.flush()
# mutex.release()