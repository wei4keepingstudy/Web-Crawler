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

def find_u(s, final_url, qq_list, num2):
	'''  '''

	dest_text = open('info.txt', 'a')
	user_list = []
	for line in qq_list:
		user = line.strip()
		try:
			#int(user)
			user_list.append(user)
		except Exception, e:
			# print 'e: ', e
			continue

	while 1:
		try:
			res = s.get(final_url, timeout=15)
			break
		except Exception, e:
			print 'e: ', e
			print 'request final url time out. try again...'
			time.sleep(10)

	post_data = {
		"num":"20",
		"page":"0",
		"sessionid":"0",
		"agerg":"0",
		"sex":"0",
		"firston":"1",
		"video":"0",
		"country":"0",
		"province":"0",
		"city":"0",
		"district":"0",
		"hcountry":"0",
		"hprovince":"0",
		"hcity":"0",
		"hdistrict":"0",
		"online":"1"
	}

	# print 'res: ', res.text

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
		post_data.update({'ldw':skey})
	except:
		pass

	while 1:
		try:
			cred_url = 'http://cgi.find.qq.com/qqfind/lbs/get_auth_flag?ldw=%s' % skey
			cred = s.get(cred_url, timeout=30)
			break
		except Exception, e:
			print 'e: ', e
			print 'request timeout: ', cred_url
			time.sleep(10)

	cred_text = cred.text
	print 'cred text: ', cred_text
	if cred_text == '{"retcode":100021}':
		print 'Not Allowed'
		return

	num = 1
	for q in user_list:
		num += 1
		if num >= len(user_list):
			print 'Time: %s ..这个用户已请求%s次，退出，休息一下，再来' % (str(num2), len(user_list))
			break;
		post_data["keyword"] = q

		#print 'post_data: ', post_data

		print u'开始验证第%s个用户...' % num
		try:
			f_url = 'http://cgi.find.qq.com/qqfind/buddy/search_v3'
			res2 = s.post(f_url, data=post_data, timeout=60)
			print '########################################\n',

			print 'res2_text: ', res2.text
			target_json = res2.json()
			if not target_json:
				print 'not target_json...'
				continue
		except Exception, e:
			print 'e: ', e
			print 'Request final url time out! drop user: ', q
			time.sleep(10)
			continue

		# target_json = target_json.replace('\'', '"')
		# print 'target_json: ', target_json
		try:
			page = target_json.get('result').get('buddy').get('page')
			if page or page == 0:
				print 'json: ', target_json
				print '########################'
				print 'oh no ...page!!!'
				continue

			target_json.update({'qq':q})
			r_json = json.dumps(target_json, ensure_ascii=False)
			dest_text.write(r_json.encode('utf8') + '\n')
			dest_text.flush()
			print 'write json to data. Time: ', num2
		except Exception, e:
			print 'e: ', e
			continue

		time.sleep(2)

	del s
	print 'del s, Time: ', num2
	dest_text.close()

def find_cookie(username, passwd, qq_list, num2):
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
	print 'd1: ', d1
	print '###################################################'

	res_1_text = res_1.text
	#print 'res_1_text:', res_1_text
	py_obj = py(res_1_text)
	script_content = py_obj('script').eq(0)
	script_con = script_content.html()
	print 'script: ', script_con
	script_1 = script_con[758:-3]
	print 'script_1: ', script_1
	print '###################################################'
	login_sig = repr(script_1).strip()[307:371]
	print 'login_sig: ', login_sig
	print '###################################################'

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
	print 'd2: ', d2

	check_vc_text = res_vc.text
	print '###################################################'
	print 'check_vc_text: ', check_vc_text
	vc_text_list = check_vc_text[13:-2].replace("'", '').split(',')

	verifycode= vc_text_list[1].strip()
	pt_verifysession_v1 = vc_text_list[3].strip()
	uin = str(vc_text_list[2])

	print '###################################################'
	print 'pt_verifysession_v1: ', pt_verifysession_v1
	print 'verifycode: ', verifycode
	print 'uin: ', uin
	print '###################################################'

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
	print 'res3: ', res3_text
	res3_list = res3_text[7:-2].replace("'", '').split(',')
	final_url = res3_list[2]
	print 'final_url: ', final_url
	if not final_url:
		print 'login failed..'
		return

	find_u(s, final_url, qq_list, num2)

def main():
	username = '312201325'
	passwd = 'yilifang123'
	num = 0
	sfile = open('qq.txt', 'r')
	cnt = 0
	while 1:
		
		qq_list = set()
		for i in xrange(10000):
			line = sfile.readline().strip().replace('"', '')
			cnt += 1
			if cnt < 210000: continue
			if len(re.findall('^(\d+)@qq\.com$', line)) == 0:
				qq_list.add(line)
		if len(qq_list) == 0: continue
		num += 1
		print 'num: ', num
		find_cookie(username, passwd, qq_list, num)
		print 'cnt:', cnt
		if num == 3:
			print 'num: ', num
			print '当前完成第%s轮请求..' % str(num)
			break

		print '当前完成第%s轮请求..' % str(num)

	print '任务完成，总共完成%s轮请求..' % str(num)

if __name__ == '__main__':
	main()
