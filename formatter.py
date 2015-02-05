#!/usr/bin/env python
"""
Used to format the raw data text files produced by a BITalino
Parses the json-text format into clean JSON more appropriate for the MATL application
"""

import sys
import json

def main():
	try:
		with open(sys.argv[1], "r") as BITfile:
			data = BITfile.read()
			header = headerToDict(data)
			print json.dumps(header)
	except IndexError as e:
		print "Missing BITalino data file argument"

"""
Parses the json data in the BITalino header into a Python dict
"""
def headerToDict(BITdatastr):
	return json.loads(BITdatastr.split("\n")[1][2:])

if __name__ == '__main__':
    main()
