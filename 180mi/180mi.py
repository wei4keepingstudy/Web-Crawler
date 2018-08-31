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
import requests
import socket
## 这段代码是用于解决中文报错的问题 
reload(sys) 
sys.setdefaultencoding("utf8") 
#####################################################
#跑到27了
# serial = []
finalfile = open("test.txt","w+")
s = requests.Session()
url = 'http://www.180mi.com/mtzz/zzmaintain.dhtml'
headers = {
	'Host':'www.180mi.com',
	'Origin':'http://www.180mi.com',
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'
}
# req = urllib2.Request(url,None,headers)
while True:

	try:
		response = s.get(
			url,
			headers = headers
			)
		break
	except Exception,e:
		print e
result = response.text
doc = pq(result.decode("utf-8"))
# print result
brandId_length = len(doc("select[id = 'ds']").find("option"))
print brandId_length
for i in range(29,brandId_length):
	brandId = doc("select[id = 'ds']").find("option").eq(i).attr("value")
	evalue = doc("select[id = 'ds']").find("option").eq(i).attr("evalue")
	# print brandId
	brandName = doc("select[id = 'ds']").find("option").eq(i).text()

	url_dept = "http://www.180mi.com/mtzz/getdept.dhtml"
	post_dept ={
		"brandId":brandId
		}
	# req_dept = urllib2.Request(url_dept,post_dept,headers)

	while True:
		try:
			response_dept = s.post(
				url_dept,
				headers = headers,
				data = post_dept
				)
			break
		except Exception,e:
			print e
	# print response_dept.read()
	result_dept = response_dept.text
	length_dept = len(json.loads(result_dept))
	serial = [[] for jj in range(length_dept)]
	for j in  range(length_dept):
		deptId = json.loads(result_dept)[j]["DEPTID"]
		bName = json.loads(result_dept)[j]["BRANDNAME"]
		dName = json.loads(result_dept)[j]["DEPTNAME"]
		deptName = bName + "--" + dName
		# print deptName

		url_style = "http://www.180mi.com/mtzz/getstyleById.dhtml"
		post_style = {
			"deptId" : deptId
			}
		# req_style = urllib2.Request(url_style,post_style,headers)
		while True:
			try:
				response_style = s.post(
					url_style,
					headers = headers,
					data = post_style
					)
				break
			except Exception,e:
				print e
		result_style = response_style.text.decode("utf-8")
		length_style = len(json.loads(result_style))
		# print length_style
		model = [[] for kk in range(length_style)]
		for k in range(length_style):
			styleId = json.loads(result_style)[k]["STYLEID"]
			styleName = json.loads(result_style)[k]["STYLENAME"]
			# print styleName
			url_add = "http://www.180mi.com/frontnew/addStyleS.dhtml"
			post_add ={
				"stylesession.brandId":evalue,
				"stylesession.deptId":deptId,
				"stylesession.styleId":styleId,
				"stylesession.styleName":styleName,
				"stylesession.deptName":deptName,
				"stylesession.brandName":brandName
				}
			# print post_add
			# req_add = urllib2.Request(url_add,post_add,headers)
			while True:
				try:
					response_add = s.post(
						url_add,
						headers = headers,
						data = post_add
						)
					break
				except Exception,e:
					print e
			# print "~" + response_add.read()
			#################################

			url_final = "http://www.180mi.com/mtzz/zzmaintain.dhtml"
			header = {
				'Host':'www.180mi.com',
				'Origin':'http://www.180mi.com',
				# 'Cookie':'jsessionid=3929CE796E2156557DD34A6EBE1A10D4-n1.tomcat2; Hm_lvt_97e500115a17ecca32f45ecdf5a89d44=1414497642; Hm_lpvt_97e500115a17ecca32f45ecdf5a89d44=1414580461',
				'Referer':'http://www.180mi.com/mtzz/zzmaintain.dhtml',
				'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36'
			}
			post_final = {
				'mileage':5000,
				'zzdata':'2014-10-30',
				'bds.styleId':brandId,
				'bds.styleId':deptId,
				'bds.styleId':styleId,

			}
			while True:
				try:
					response_final = s.post(
						url_final,
						headers = header,
						data = post_final
						)
					break
				except Exception,e:
					print e
			doc_final = pq(response_final.text.decode("utf-8"))
			maintain = doc_final("span[class = 'floatLeft']").text()
			# print styleName +maintain

			maintain_first_flag_index1 = maintain.find("：")
			maintain_first_flag_index2 = maintain.find("/")
			maintain_first_flag = maintain[maintain_first_flag_index1 + 1:maintain_first_flag_index2]
			maintain_first_period_index = maintain.find(" ")
			maintain_first_period = maintain[maintain_first_flag_index2+1:maintain_first_period_index]

			maintain_second_flag_index1 = maintain.find("：",30)
			maintain_second_flag_index2 = maintain.find("/",30)
			maintain_second_flag = maintain[maintain_second_flag_index1+1:maintain_second_flag_index2]
			maintain_second_period_index = maintain.find(" ",40)
			maintain_second_period = maintain[maintain_second_flag_index2+1:maintain_second_period_index]

			maintain_per_flag_index1 = maintain.find("：",60)
			maintain_per_flag_index2 = maintain.find("/",60)
			maintain_per_flag = maintain[maintain_per_flag_index1+1:maintain_per_flag_index2]
			maintain_per_period_index = maintain.find(" ",70)
			maintain_per_period = maintain[maintain_per_flag_index2+1:maintain_per_period_index]
			if  not doc_final("table[id = 'maintaincontainer']"):
				 maintain_first_flag = "None"
				 maintain_first_period = "None"
				 maintain_second_flag = "None"
				 maintain_second_period= "None"
				 maintain_per_flag= "None"
				 maintain_per_period= "None"

			first = {"maintainName":"首保",
				"mileageFlag": maintain_first_flag,
				"monthPeriod": maintain_first_period
				}
			second = {"maintainName":"二保",
				"mileageFlag": maintain_second_flag,
				"monthPeriod": maintain_second_period
				}
			period = {"maintainName":"间隔",
				"mileageFlag": maintain_per_flag,
				"monthPeriod": maintain_per_period
				}
			maintainPlan = {"first" : first,"second" : second, "period" : period}
			# print maintainPlan

			tr_length = len(doc_final("table[id = 'maintaincontainer']").find("tr"))
			td_length = len(doc_final("table[id = 'maintaincontainer']").find("tr").eq(0).find("td"))
			lists = [[] for ye in range(td_length)]

			for tr in range(tr_length-1):
				# td_length = len(doc_final("table[id = 'maintaincontainer']").find("tr").eq(tr).find("td"))
				# lists = [[] for ye in range(td_length)]
				# print td_length
				for td in range(td_length):
					if tr == 0 :
						milageFlag = doc_final("table[id = 'maintaincontainer']").find("tr").eq(0).find("td").eq(td).text()
						lists[td].append(milageFlag)
				# print lists
					# elif tr == int(tr_length):
					# 	total = doc_final("table[id = 'maintaincontainer']").find("tr").eq(tr).find("td").eq(td).text()
					# 	lists[td].append(total)
					else:
						if td != 0 or 1:
							if  doc_final("table[id = 'maintaincontainer']").find("tr").eq(tr).find("td").eq(td).attr("value") is not "0":
								itemName = doc_final("table[id = 'maintaincontainer']").find("tr").eq(tr).find("td").eq(0).text()
								price = doc_final("table[id = 'maintaincontainer']").find("tr").eq(tr).find("td").eq(1).text()
								lists[td].append(itemName)
								lists[td].append(price)
								# print lists
			if   not doc_final("table[id = 'maintaincontainer']"):
				lists = ["There is no fitable data"]
			else :
				del lists[0]
				del lists[0]
			# print json.dumps(lists, ensure_ascii=False)
			# maindata = {"maindata" : lists}
			# print maindata
	
			model[k] = [{"model" : styleName,
				"maintainPlan" : maintainPlan,
				"maindata" : lists
				}]
		# print json.dumps(model, ensure_ascii=False)
			# print model
		serial[j] = [{"serialName" : dName,
			"model" : model
			}]
	# print json.dumps(serial, ensure_ascii=False)
	finaljs= {"brand" : brandName,
		"serial" : serial
		}


	finalfile.write(json.dumps(finaljs, ensure_ascii=False) + "\n")
	print i
	finalfile.flush()