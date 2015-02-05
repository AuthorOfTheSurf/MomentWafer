#!/usr/bin/env python
"""
Used to format the raw data text files produced by a BITalino
Parses the json-text format into clean JSON more appropriate for the MATL application
"""

import sys

def main():
	try:
		with open(sys.argv[1], "r") as bitalinoData:
			data = bitalinoData.read()
			print data
	except IndexError as e:
		print "Missing BITalino data file argument"

if __name__ == '__main__':
    main()
