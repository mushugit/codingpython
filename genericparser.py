from bs4 import BeautifulSoup
import urllib
import re
import os

import sys, getopt

scriptname = "genericparser.py"
usagetext = scriptname + " -u <urltoparse> -p <parseparameterfile>"

def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hu:p:",["url=","pfile="])
	except getopt.GetoptError:
		print usagetext
		sys.exit(2)
		for opt, arg in opts:
			if opt == '-h':
				print usagetext
				sys.exit()
			elif opt in ("-u", "--url"):
				inputfile = arg
			elif opt in ("-p", "--pfile"):
				outputfile = arg
				print 'Url is "', inputfile							
				print 'Parse parameter file is "', outputfile


if __name__ == "__main__":
   main(sys.argv[1:])

'''
modsurlwithpage = modsurl + str(pagenum)
soup = BeautifulSoup(urllib.urlopen(modsurlwithpage).read())
'''
