#!/usr/bin/env python
"""
Used to format the raw data text files produced by a BITalino
Parses the json-text format into clean JSON more appropriate for the MATL application
"""

import sys
import json

class BITalinoData:
	"""
	Constructor
	"""
	def __init__(self, BITalinoTxtData=""):
		self._dataStream = BITalinoTxtData.split("\n")
		self._header = json.loads(self._dataStream[1][2:])
		self._channels = {}
	"""
	BITalino header as a Python dict
		{
			"SamplingResolution": "10",
			"SampledChannels": [1],
			"SamplingFrequency": "1000",
			"ColumnLabels": ["SeqN", "Digital0", "Digital1", "Digital2", "Digital3", "EMG"],
			"AcquiringDevice": "98:D3:31:B2:BD:4F",
			"Version": "111",
			"StartDateTime": "2015-2-2 10:30:2"
		}

	"""
	@property
	def header(self):
	    return self._header
	@header.setter
	def header(self, value):
	    self._header = value
	"""
	Raw multi-column data stream, array of tsv
	The "Digital*" channels are not recording data in this instance
	SeqN resets every 16 samples

		| SeqN | Digital0 | Digital1 | Digital2 | Digital3 | EMG |
		15	1	1	1	1	270	
		0	1	1	1	1	551	
		1	1	1	1	1	432	
	"""
	@property
	def dataStream(self):
	    return self._dataStream
	@dataStream.setter
	def dataStream(self, value):
	    self._dataStream = value
	"""
	List of the channels and their data
		[
			{ "label": "EMG", "data": [270, 551, 432] }
		]
	"""
	@property
	def channels(self):
	    return self._channels
	@channels.setter
	def channels(self, value):
	    self._channels = value

	
def main():
	try:
		with open(sys.argv[1], "r") as bitsrc:
			data = BITalinoData(bitsrc.read())
			print json.dumps(data.header)
	except IndexError as e:
		print "Missing BITalino data file argument"

if __name__ == '__main__':
    main()
