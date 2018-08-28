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
## 这段代码是用于解决中文报错的问题 
reload(sys) 
sys.setdefaultencoding("utf8") 
#####################################################
s = requests.Session()
class ThreadUrl(threading.Thread):

	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def spider(self):
		while True:
			dict_url = self.queue.get()
			qqid = dict_url.get("qqid")
			response_1 = dict_url.get("response_1")
			while True:
				try:
					
					# url_1 = 'http://q32.3g.qq.com/g/s?aid=nqqchatMain&sid=AbsAO-xJ_b1RaF9ieYFqXKsP&myqq=1664317189'
					# headers = {
					# 	'Host':'q32.3g.qq.com',
					# 	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'
					# }
					# response_1 = s.get(
					# 	url_1,
					# 	headers = headers
					# 	)
					# print response_1.text
					doc = pq(response_1.content)
					url_find = doc("div[class = 'main-module']").find('a').eq(3).attr('href')
					# print url_find
					url_sp = url_find.replace("http://q16.3g.qq.com","http://q32.3g.qq.com")
					url_get = url_sp + "nqqUserInfo"
					headers_get = {
						'Host':'q32.3g.qq.com',
						'Origin':'http://q16.3g.qq.com',
						'Referer':url_find,
						'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'
					}
					postData = {
						'u':qqid
					}
					response_get = s.post(
						url_get,
						headers = headers_get,
						data = postData
						)
					# # print response_get.text
					qqList1 = ["QQnumber","nickname","sign","sex","age","country","province","address","phone","mobile","Email"]
					doc_get = pq(bytes(bytearray(response_get.content,encoding = "utf-8")),parser='html_fragments')
					# # print type(doc_get)
					# # (bytes(bytearray(text, encoding='utf-8')), parser='html')
					nick_name = doc_get("div[class = 'main-module bm-gray']").eq(1).find('p').eq(0).text()
					nickna_me = nick_name.replace("昵称："," ")
					nickname = nickna_me.replace("变为金色", " ")
					# print nick_name
					s_ign = doc_get("div[class = 'main-module bm-gray']").eq(1).find('p').eq(2).text()
					sign = s_ign.replace("个性签名："," ")
					se_x = doc_get("div[class = 'main-module bm-gray']").eq(4).find('p').text()
					sex = se_x.replace("性别："," ")
					ag_e = doc_get("div[class = 'main-module bm-gray']").eq(5).find('p').text()
					age = ag_e.replace("年龄："," ")
					coun_try = doc_get("div[class = 'main-module bm-gray']").eq(6).find('p').text()
					country = coun_try.replace("国家："," ")
					provin_ce = doc_get("div[class = 'main-module bm-gray']").eq(7).find('p').text()
					province = provin_ce.replace("省份："," ")
					add_ress = doc_get("div[class = 'main-module bm-gray']").eq(8).find('p').text()
					address = add_ress.replace("地址："," ")
					ph_one = doc_get("div[class = 'main-module bm-gray']").eq(9).find('p').text()
					phone = ph_one.replace("电话："," ")
					mo_bile = doc_get("div[class = 'main-module bm-gray']").eq(10).find('p').text()
					mobile = mo_bile.replace("手机："," ")
					E_mail = doc_get("div[class = 'main-module bm-gray']").eq(11).find('p').text()
					Email = E_mail.replace("Email："," ")
					qqList2 = [qqid,nickname,sign,sex,age,country,province,address,phone,mobile,Email]
					qqList = dict(zip(qqList1,qqList2))
					# # print qqList
					qqjs = json.loads(json.dumps(qqList))
					print json.dumps(qqjs)
					time.sleep(20)
					# break
				except Exception , e:
					print e
			self.queue.task_done()

	def run(self):
		self.spider()
def main():
	queue = Queue.Queue()
	url = 'http://pt.3g.qq.com/psw3gqqLogin?r=389885325&vdata=11B56D4922B508A599273CC007BCDDA7'
	headers = {
		'Host':'pt.3g.qq.com',
		'Origin':'http://pt.3g.qq.com',
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'
	}
	postdata = {
		'qq':'1664317189',
		'pwd':'longhu123',
		'bid_code':'3GQQ',
		'toQQchat':'true',
		'login_url':'http://pt.3g.qq.com/s?aid=nLoginnew&q_from=3GQQ',
		'q_from':'3GQQ',
		'modifySKey':'0',
		'loginType':'1',
		'aid':'nLoginHandle',
		'i_p_w':'qq|pwd|'
	}
	response = s.post(
		url,
		headers = headers,
		data = postdata,
		allow_redirects = False
		)
	url_1 = 'http://q32.3g.qq.com/g/s?aid=nqqchatMain&sid=AbsAO-xJ_b1RaF9ieYFqXKsP&myqq=1664317189'
	headers = {
		'Host':'q32.3g.qq.com',
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'
	}
	response_1 = s.get(
		url_1,
		headers = headers
		)
	# print response.status_code

	# data = response.content
	# input_file = open('****************','r+')
	# for eachline in input_file:
	# 	qqid = eachline.strip()
	# 	queue.put(qqid)
	for i in range(1000):
		dict_url= {"qqid":565168510, "response_1":response_1}
		queue.put(dict_url)
	threadlist = []
	for i in range(3):
		t = ThreadUrl(queue)
		threadlist.append(t)
		t.start()

	for each in threadlist:
		each.join()

if __name__ == '__main__':
	main()