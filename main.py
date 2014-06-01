#! /usr/bin/env python

from scanner import scanner
import sys
import getopt
import re

error = 'Finished!'

def mgetopt():
	global error
	try:
		opts = getopt.getopt(sys.argv[1:], 'r:t:v')
		opts = {i[0]:i[1] for i in opts[0]}
		if re.findall('^http://[\w\.-]+(?::\d+)?/$', opts['-r'])[0] != opts['-r']:
			raise
		if opts.has_key('-t'):
			opts['-t'] = int(opts['-t'])
		return opts
	except:
		error = 'Bad Parameter!'
		return None

def main():
	opts = mgetopt()
	if opts:
		scanner()

if __name__ == '__main__':
	main()
	print >> sys.stderr, error
