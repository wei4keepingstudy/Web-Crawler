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

def main(qqid):
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
	# print response.status_code

	data = response.text
	# print data
	url_1 = 'http://q32.3g.qq.com/g/s?aid=nqqchatMain&sid=AbsAO-xJ_b1RaF9ieYFqXKsP&myqq=1664317189'
	headers = {
		'Host':'q32.3g.qq.com',
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'
	}
	response_1 = s.get(
		url_1,
		headers = headers
		)

	doc = pq(response_1.content)
	url_find = doc("div[class = 'main-module']").find('a').eq(3).attr('href')
	href_index = url_find.index('/',10)
	url_sp = url_find[href_index:]
	url_get = "http://q32.3g.qq.com" + str(url_sp) + "nqqUserInfo"
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

	# print response_get.text
	qqList1 = ["QQnumber","nickname","sign","sex","age","country","province","address","phone","mobile","Email"]
	doc_get = pq(response_get.content.decode("utf-8","ignore"))
	nick_name  = doc_get("div[class = 'main-module bm-gray']").eq(1).find('p').eq(0).text()
	nickname = nick_name.split(' ')[1]
	print nickname
	s_ign = doc_get("div[class = 'main-module bm-gray']").eq(1).find('p').eq(2).text()
	sign = s_ign.replace("个性签名："," ")
	print sign
	se_x = doc_get("div[class = 'main-module bm-gray']").eq(4).find('p').text()
	sex = se_x.replace("性别："," ")
	print sex
	ag_e = doc_get("div[class = 'main-module bm-gray']").eq(5).find('p').text()
	age = ag_e.replace("年龄："," ")
	print age
	coun_try = doc_get("div[class = 'main-module bm-gray']").eq(6).find('p').text()
	country = coun_try.replace("国家："," ")
	print country
	provin_ce = doc_get("div[class = 'main-module bm-gray']").eq(7).find('p').text()
	province = provin_ce.replace("省份："," ")
	print province
	add_ress = doc_get("div[class = 'main-module bm-gray']").eq(8).find('p').text()
	address = add_ress.replace("地址："," ")
	print address
	ph_one = doc_get("div[class = 'main-module bm-gray']").eq(9).find('p').text()
	phone = ph_one.replace("电话："," ")
	print phone
	mo_bile = doc_get("div[class = 'main-module bm-gray']").eq(10).find('p').text()
	mobile = mo_bile.replace("手机："," ")
	print mobile
	E_mail = doc_get("div[class = 'main-module bm-gray']").eq(11).find('p').text()
	Email = E_mail.replace("Email："," ")
	print Email
	qqList2 = [qqid,nickname,sign,sex,age,country,province,address,phone,mobile,Email]
	qqList = dict(zip(qqList1,qqList2))
	# # print qqList
	qqjs = json.loads(json.dumps(qqList))
	print json.dumps(qqjs)


if __name__ == '__main__':
	main(565168510)