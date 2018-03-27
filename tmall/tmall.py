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
import  requests
import urllib
import socket
## 这段代码是用于解决中文报错的问题 
reload(sys) 
sys.setdefaultencoding("utf8") 
#####################################################
mutex = threading.Lock()
file_tmall = open('tmall.txt','w+')
cantget_id =  open("cantget_id.txt","w+")
unfinish_id = open("unfinish_id.txt","w+")
strangeWeb = open("strangeWeb.txt","a+")

header = {
	# "Cookie":"cna=oZz0DJcqPxYCAba XeNb5uuED; _tb_token_=DYnlJD24LViK; uc3=nk2=AGiWgxFL6CXP&id2=UojWl%2FVCPxHp1A%3D%3D&vt3=F8dATSsNRZOMz%2FFmi%2FY%3D&lg2=UtASsssmOIJ0bQ%3D%3D; lgc=crazyvgod; tracknick=crazyvgod; cookie2=1b9546abe37e5093cbe5b4dcf0c7cf87; cookie1=Vv7MWfE6kqez2IW8DOtp8AwI9SYxJxc04%2FbymvAYyo4%3D; unb=1922391426; t=17549614bde39364c27412dc16d7db97; _l_g_=Ug%3D%3D; _nk_=crazyvgod; cookie17=UojWl%2FVCPxHp1A%3D%3D; uc1=cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&existShop=false; login=true; pnm_cku822=; isg=2381A527EBBC3A098467ACC5C942EF3B; swfstore=269352; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; whl=-1%260%260%260",
	"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36"
}
s = requests.Session()
class Threading_tmall(threading.Thread):
	"""docstring for Threading_douban"""
	def __init__(self, tmall_queue):
		threading.Thread.__init__(self)
		self.tmall_queue = tmall_queue

	def get_record(self):		
		while True:
			if self.tmall_queue.empty():
				break
			urlId = self.tmall_queue.get()
			while True:
				try:
					url = "http://store.taobao.com/search.htm?user_number_id=" + str(urlId) + "&orderType=hotsell_desc"
					# print url
					response = s.get(
						url,
						headers = header
						)

					result = response.text

					if "店铺浏览-淘宝网" not in result:
						flag = 1
						if "J_TCrumbSearchForm" not in  result and "J_SearchAsync"  not in result:
							print str(urlId) + "IP has been killed!!!!!!!!!"
							flag += 1
							if flag >15:
								print "over 15"
								mutex.acquire()
								strangeWeb.write("urlId:" + str(urlId)  + "\t" + "\n")
								strangeWeb.flush()
								mutex.release()
								break
							else:
								continue
							# else:
							# 	pass
						else:
							doc = pq(result)
							if doc("b[class = 'ui-page-s-len']"):

								length_res = doc("b[class = 'ui-page-s-len']").text()
								# print length_res
								start = length_res.find("/")
								length = length_res[start+1:]

								self.get_result(urlId,length)
							elif doc("span[class =  'page-info']"):
								length_res = doc("span[class =  'page-info']").text()
								start = length_res.find("/")
								length = length_res[start+1:]
								self.get_result(urlId,length)
							else:
								length = 0
								self.get_result(urlId,length)

					else:
						length = 0
						self.get_result(urlId,length)		
					break
					
				except Exception, e:
					print e 
					time.sleep(1)
					mutex.acquire()
					unfinish_id.write(str(e) + "\t" + "urlId:" + str(urlId)  + "\t" + "\n")
					unfinish_id.flush()
					mutex.release()
			self.tmall_queue.task_done()

	def get_result(self,urlId,length):
		global file_tmall		
		detail = []
		while True:
			try:
				# print length

				if length  == 0:
					detail = "该商铺已经关闭或存在其它异常"
				for i in range(1,int(length)+1):
					url_get = "http://store.taobao.com/search.htm?user_number_id=" + str(urlId) + "&orderType=hotsell_desc&pageNo=" + str(i)

					response_get= s.get(
						url_get,
						headers = header
						)
					result_get = response_get.text
					flag = 1
					if "J_TCrumbSearchForm" not in  result_get and "J_SearchAsync"  not in result_get	:
						print str(urlId) + "IP has been killed!!!!!!!!!"
						flag += 1
						if flag >15:
							print "over 15"
							mutex.acquire()
							strangeWeb.write("urlId:" + str(urlId)  + "\t" + "\n")
							strangeWeb.flush()
							mutex.release()
							break
						else:
							continue
					else:
						doc_get = pq(result_get)

						length_get = len(doc_get("div[class = 'J_TItems']").find("dl")(".thumb"))

						print length_get
						for j in range(length_get):
							
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
							each_detail = {
								"title" : title,
								"price" : price,
								"salenum" : salenum,
								"commentsNum" : comments
							}
							detail.append(each_detail)

				record = {
					"urlId":urlId,
					"detail" : detail
				}
				json_record = json.loads(json.dumps(record))
				mutex.acquire()
				file_tmall.write(json.dumps(json_record, ensure_ascii=False) + "\n")
				# print "1"
				file_tmall.flush()
				mutex.release()

				break

			except Exception,e:
				# s=sys.exc_info()
				# print s[2].tb_lineno
				print e 
				time.sleep(1)
				mutex.acquire()
				cantget_id.write(str(e) + "urlId : " + urlId + "\n")
				cantget_id.flush()
				mutex.release()



	def run(self):
		self.get_record()


def main():
	tmall_queue = Queue.Queue()
	# for i in range(100):
	while True:
		try:
			input_data = open("seed_shop_items_20141118.json","r")
			for line in input_data:
				json_line = json.loads(line)
				urlId= json_line.get("seller_id").strip()

				tmall_queue.put(urlId)
			break
		except Exception, e:
			
			print e, "records_queue_put_fail"

	threadlist = []

	for i in range(20):
		Thread_get_record = Threading_tmall(tmall_queue)
		threadlist.append(Thread_get_record)
		Thread_get_record.start()

	for each in threadlist:
		each.join()

if __name__ == '__main__':
	main()
