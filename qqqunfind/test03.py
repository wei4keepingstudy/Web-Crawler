def main():
	qqqun_queue = Queue.Queue()
	username = '1507866731'
	passwd = 'yilifang123'
	

		
		
		sfile = open('cd_qunid.txt', 'r')
		
		for line in sfile:
			qqqunNum = line.strip()
			qun_dict = [s,final_url,qqqunNum]
			qqqun_queue.put(qun_dict)
					# print qun_dict
			
		# find_cookie(username, passwd, qq_list, num)
	find_cookie(username, passwd)
	threadlist = []


class ProducerThread(threading.Thread):
	def __init__(self, weibo_queue):
		threading.Thread.__init__(self)
		self.weibo_queue = weibo_queue
	def run(self):
		users = open("id.txt","r")
		for username in 
		input_data = open('cd_qunid.txt', 'r')
		# print len(input_data.readlines())
		while True:
			lines = input_data.readlines(300)
			if not lines:
				break
			else:
				for line in lines:
					qqqunNum = line.strip()
					qun_dict = [s,final_url,qqqunNum]
					qqqun_queue.put(qun_dict)
				if not self.weibo_queue.empty() :
					print "over5"
					time.sleep(600)


def main():
	weibo_queue = Queue.Queue(300)
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

	def find_cookie(username, passwd):
		
		final_url = res3_list[2]
		# print 'final_url: ', final_url
		if not final_url:	
			print 'login failed..'
			return




	threadlist = []
	find_cookie(username, passwd)
	print 'start******'
	for i in range(20):
		Thread_get_record = Threading_qqqun(qqqun_queue)
		threadlist.append(Thread_get_record)
		Thread_get_record.start()

	Thread_get_23 = ProducerThread(weibo_queue)
	threadlist.append(Thread_get_23)
	Thread_get_23.start()

	for each in threadlist:
		each.join()

if __name__ == '__main__':
	main()
