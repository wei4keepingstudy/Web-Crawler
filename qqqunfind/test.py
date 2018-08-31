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

# cgitb.enable(context=10, format='text')

def _hexchar2bin(sstr):
	slist = ''
	i = 0
	while 1:
		b = sstr[i:i+2]
		if not b:
			break
		slist += chr(int(b, 16))
		i += 2
	return slist

def _getEncryption(password, uin, vcode):
	x = hashlib.md5(password).hexdigest().upper()

	str1 = _hexchar2bin(x)
	str2 = hashlib.md5(str1 + uin).hexdigest().upper();
	str3 = hashlib.md5(str2 + vcode.upper()).hexdigest().upper();
	return str3

def get_skey_code(e):
	n=5381
	for i in e:
		temp = n<<5
		n+=int(temp)+int(ord(i))
		m = longToInt(n)
		# print 'm: ', m
	return m

def longToInt(value):
	if value > 2147483647:
		return (value & (2 ** 31 - 1))
	else:
		return value

def find_u(s, final_url, qq_list):
	'''  '''

	dest_text = open('info.txt', 'a+')
	user_list = []
	for line in qq_list:
		user = line.strip()
		try:
			#int(user)
			user_list.append(user)
		except Exception, e:
			# print 'e: ', e
			continue

	post_data = {
		"n":"24",
		"st":"1",
		"iso":"1",
		"src":"1",
		"v":"4903",
		"p":"0",
		"guagua":"1",
		"guaguan":"3",
		"isRecommend":"false",
		"city_id":"0",
		"from":"1"
	}
	data01  ={
		"guagua":"1",
		"ver":"4903"
	}
	data02 = {
		"n":"6",
		"st":"1",
		"guagua":"1",
		"guaguan":"1",
		"v":"4903",
		"src":"1",
		"gdt":"1",
		"gdtn":"1",
	}

	# print 'res: ', res.text
	while 1:
		try:
			res = s.get(final_url, timeout=15)
			break
		except Exception, e:
			print 'e: ', e
			print 'request final url time out. try again...'
			time.sleep(10)
	while 1:
		try:
			first = s.get('http://find.qq.com', timeout=30)
			break
		except Exception, e:
			print 'e: ', e
			print 'request find.qq.com timeout'
			time.sleep(10)

	# print 's: ', first.text
	sk = s.cookies
	try:
		skey_b = sk.get('skey')
		skey = get_skey_code(skey_b)
		print "skey____" + str(skey)
		post_data.update({'ldw':skey})
		data01.update({'ldw':skey})
		data02.update({'ldw':skey})
	except:
		pass

	test_login = test(s,post_data,data01,data02)
	if test_login == 0:
		print "该账号已被封禁"
		time.sleep(5000)
	print " 该用户未被封禁"
		

	for q in user_list:

		print q
		post_data["k"] = q

		qun_url01 = "http://cgi.find.qq.com/qqfind/group/hotwords_v2"
		while 1:
			try:
				response01 = s.post(qun_url01,data = data01,timeout = 60)
				break
			except Exception,e:
				print e
			# print "response01"

		qun_url02 = "http://cgi.find.qq.com/qqfind/qun/rcmd_v5"
		while 1:
			try:
				response02 = s.post(qun_url02,data = data02,timeout = 60)
				break
			except Exception,e:
				print e
			# print "response02"
		try :
			f_url = 'http://cgi.find.qq.com/qqfind/qun/search_group_rcmd_v6'
			res2 = s.post(f_url, data=post_data, timeout=60)
			print '########################################\n',

			# print 'res2_text: \t', res2.text
			target_json = res2.json()
			if res2.text == '{"retcode":100000}':
				print 'Not Allowed'
				time.sleep(20)
				continue
		except Exception, e:
			print 'e: ', e
			print 'Request final url time out! drop user: ', q
			time.sleep(10)
			continue

		# target_json = target_json.replace('\'', '"')
		# print 'target_json: ', target_json
		try:
			target_json.update({'qqqunNum':q})
			r_json = json.dumps(target_json, ensure_ascii=False)
			dest_text.write(r_json.encode('utf8') + '\n')
			dest_text.flush()
		except Exception, e:
			print 'e: ', e
			continue

		time.sleep(2)

	del s
	
	dest_text.close()
def test(s,post_data,data01,data02):
	q = "1686653"
	post_data["k"] = q
	qun_url01 = "http://cgi.find.qq.com/qqfind/group/hotwords_v2"
	while 1:
		try:
			response01 = s.post(qun_url01,data = data01,timeout = 60)
			break
		except Exception,e:
			print e
		# print "response01"

	qun_url02 = "http://cgi.find.qq.com/qqfind/qun/rcmd_v5"
	while 1:
		try:
			response02 = s.post(qun_url02,data = data02,timeout = 60)
			break
		except Exception,e:
			print e
		# print "response02"
	while True:
		try :
			f_url = 'http://cgi.find.qq.com/qqfind/qun/search_group_rcmd_v6'
			res2 = s.post(f_url, data=post_data, timeout=60)
			break
			# print '########################################\n',
		except Exception, e:
			print 'e: ', e
	result = res2.text
	if ":{}"  in result:
		return 0



def find_cookie(username, passwd, qq_list):
	'''  '''
	url = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=46000101&style=23&s_url=http://t.qq.com&daid=6'

	s = requests.Session()
	while 1:
		try:
			res_1 = s.get(url, timeout=10)
			break
		except Exception, e:
			print 'e: ', e
			print 'request login page time out. try again.'
			time.sleep(5)

	d1 = dict(res_1.cookies)
	# print 'd1: ', d1
	# print '###################################################'

	res_1_text = res_1.text
	#print 'res_1_text:', res_1_text
	py_obj = py(res_1_text)
	script_content = py_obj('script').eq(0)
	script_con = script_content.html()
	# print 'script: ', script_con
	script_1 = script_con[758:-3]
	# print 'script_1: ', script_1
	# print '###################################################'
	login_sig = repr(script_1).strip()[307:371]
	# print 'login_sig: ', login_sig
	# print '###################################################'

	url_vc = 'https://ssl.ptlogin2.qq.com/check?regmaster=&uin=%s&appid=46000101&js_ver=10090&js_type=1&login_sig=%s&u1=http://t.qq.com&r=0.8100248416885734' % (username, login_sig)

	headers1 = {
		'Referer':'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=46000101&style=23&s_url=http://t.qq.com&daid=6',
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'
	}

	while 1:
		try:
			res_vc = s.get(url_vc, timeout=5, cookies=d1, headers=headers1)
			break
		except Exception, e:
			print 'e: ', e
			print 'check regmaster time out, try again.'
			time.sleep(5)

	d2 = dict(res_vc.cookies)
	d2['uikey'] = d1['uikey']
	d2['ptui_loginuin'] = username
	# print 'd2: ', d2

	check_vc_text = res_vc.text
	# print '###################################################'
	# print 'check_vc_text: ', check_vc_text
	vc_text_list = check_vc_text[13:-2].replace("'", '').split(',')

	verifycode= vc_text_list[1].strip()
	pt_verifysession_v1 = vc_text_list[3].strip()
	uin = str(vc_text_list[2])

	# print '###################################################'
	# print 'pt_verifysession_v1: ', pt_verifysession_v1
	# print 'verifycode: ', verifycode
	# print 'uin: ', uin
	# print '###################################################'

	uin = uin.decode('string-escape')

	p = _getEncryption(passwd, uin, verifycode)
	# print 'p: ', p

	stime = repr(time.time()).replace('.', '')[:-3]
	# print 'stime: ', stime
	u1 = 'http%3A%2F%2Ft.qq.com'

	login_2_url = 'https://ssl.ptlogin2.qq.com/login?u=%s&verifycode=%s&pt_vcode_v1=0&pt_verifysession_v1=%s&p=%s&pt_rsa=0&u1=%s&ptredirect=1&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=1-46-%s&js_ver=10090&js_type=1&login_sig=%s&pt_uistyle=23&low_login_enable=1&low_login_hour=720&aid=46000101&daid=6&' % (username, verifycode, pt_verifysession_v1, p, u1, stime, login_sig)

	headers = {
		'Referer':'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=46000101&style=23&lang=&low_login=1&hide_border=1&hide_title_bar=1&hide_close_icon=1&border_radius=1&self_regurl=http://reg.t.qq.com/index.php&proxy_url=http://t.qq.com/proxy_t.html&s_url=http://t.qq.com&daid=6',
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'
	}

	while 1:
		try:
			res3 = s.get(login_2_url, timeout=5, cookies=d2, headers=headers)
			break
		except Exception, e:
			print 'e: ', e
			print 'login timeout, try again.'
			time.sleep(5)

	res3_text = res3.text
	# print 'res3: ', res3_text
	res3_list = res3_text[7:-2].replace("'", '').split(',')
	final_url = res3_list[2]
	# print 'final_url: ', final_url
	if not final_url:
		print 'login failed..'
		return 0

	find_u(s, final_url, qq_list)

def main():
	qqlogin_id = open("qqlogin.txt","r")
	sfile = open('qunidtest.txt', 'r')
	for username in qqlogin_id:
		username = username.strip()
		# print username
		passwd = 'yilifang123'		
		
		while 1:	
			qq_list = []
			for i in range(3):
				lines = sfile.readline()
				print "1"
				# print "line~~~~~~" + str(line)
				qqqunNum = lines.strip()
				qq_list.append(qqqunNum)

			cook = find_cookie(username, passwd, qq_list)
			if cook == 0:
				print "登录失败"
				time.sleep(100)
				pass
			break


if __name__ == '__main__':
	main()
