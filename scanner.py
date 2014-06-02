import curses
import threadpool
from time import sleep
from socket import gethostbyname
import sys
import re
import requests


class scanner(object):
	"""
		Monster
	"""
	def __init__(self, rootpath, threadcount):
		self.rootpath = rootpath
		self.threadcount = threadcount
		curses.setupterm()
		#lines = curses.tigetnum('lines')
		self.cols = curses.tigetnum('cols')
		if self.check() == False:
			return
		self.updatestatus('Initializing......')
		self.pool = threadpool.ThreadPool(threadcount)
		urls = []
		exts = ['rar', 'htm', 'html', 'xhtml', 'zip', 'js']
		for url in open('list.dic'):
			for ext in exts:
				urls.append(url.strip() + '.' + ext)
		self.reqs = threadpool.makeRequests(self.detect, urls)
		self.run()

	def run(self):
		[self.pool.putRequest(req) for req in self.reqs]
		self.pool.wait()

	def updatestatus(self, status):
		sys.stdout.write('%s%s\r' % (status, ' ' * (self.cols - len(status))))
		sys.stdout.flush()

	def log(self, string):
		print '%s%s' % (string, ' ' * (self.cols - len(string)))

	def test(self, x):
		sleep(x)
		self.updatestatus(str(x))

	def check(self):
		self.updatestatus('Collecting information......')
		self.hostname = re.findall('^http://([\w\.-]+)(?::\d+)?/$', self.rootpath)[0]
		ret = True
		try:
			self.ip = gethostbyname(self.hostname)
			r = requests.head(self.rootpath)
			r.headers = dict(r.headers)
			if r.headers.has_key('server'):
				self.server = r.headers['server'].strip()
			if r.headers.has_key('x-powered-by'):
				self.xpoweredby = r.headers['x-powered-by'].strip()
		except:
			ret = False
			self.ip = '0.0.0.0'
		self.log('Hostname:'.ljust(15) + self.hostname)
		self.log('IP Address:'.ljust(15) + self.ip)
		if 'server' in dir(self):
			self.log('Server:'.ljust(15) + self.server)
		if 'xpoweredby' in dir(self):
			self.log('x-powered-by:'.ljust(15) + self.xpoweredby)
		return ret
	
	def detect(self, url):
		url = self.rootpath + url
		self.updatestatus(url)
		try:
			r = requests.head(url)
			if r.status_code == 200:
				self.log(url)
		except KeyboardInterrupt:
			sys.exit()
		except:
			pass
		
