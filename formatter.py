#!/usr/bin/env python
"""
Used to format the raw data text files produced by a BITalino
Parses the json-text format into a Python object more appropriate for
processing by the the MATL application

Sample BITalino txt file:

	# JSON Text File Format
	# {"SamplingResolution": "10", "SampledChannels": [1], "SamplingFrequency": "1000", "ColumnLabels": ["SeqN", "Digital0", "Digital1", "Digital2", "Digital3", "EMG"], "AcquiringDevice": "98:D3:31:XX:XX:XX", "Version": "111", "StartDateTime": "2015-2-2 10:30:2"}
	# EndOfHeader
	0	1	1	1	1	467	
	1	1	1	1	1	467	
	2	1	1	1	1	472	
	3	1	1	1	1	476	
	4	1	1	1	1	478	
	...

"""

import sys
import json
import numpy

class BITalinoData:
	"""
	Constructor
	"""
	def __init__(self, BITalinoTxtData):
		split = BITalinoTxtData.split("\r\n")
		self._dataStream = split[3:]
		self._header = json.loads(split[1][2:])
		self._channels = self.makeChannels(self._dataStream)
	"""
	BITalino header as a Python dict
		{
			"SamplingResolution": "10",
			"SampledChannels": [1],
			"SamplingFrequency": "1000",
			"ColumnLabels": ["SeqN", "Digital0", "Digital1", "Digital2", "Digital3", "EMG"],
			"AcquiringDevice": "98:D3:31:XX:XX:XX",
			"Version": "111",
			"StartDateTime": "2015-2-2 10:30:2"
		}
	"""
	@property
	def header(self):
	    return self._header
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
	"""
	List of the channels and their data
		[
			{ "label": "Digital0", "data": [1, 1, 1] },
			...
			{ "label": "EMG", "data": [270, 551, 432] }
		]
	"""
	@property
	def channels(self):
	    return self._channels
	"""
	Parses the dataStream into and array of channel objects containing data and a label.
	See the description for BITalinoData.channels
	"""
	def makeChannels(self, dataStream):
		channels = []
		labels = self._header["ColumnLabels"]
		# Each line has a trailing tab, Datastream ends with a blank line
		cleanStream = [line[:-1].split("\t") for line in dataStream[:-1]]
		for col in range(len(labels)):
			if col != 0:
				# Convert to numpy.array then each column becomes the channel's data
				# Also include label for the data
				channels.append({
					"label": labels[col],
					"data": numpy.array(cleanStream)[:,col]
				})
		return channels
	"""
	Return a JSON representation of this BITalinoData object
	"""
	def toJson(self, pretty=True):
		jsonCh = [{"label": ch["label"], "data": ch["data"].tolist()} for ch in self._channels]
		return json.dumps({ "header": self._header, "channels": jsonCh })

def main():
	try:
		with open(sys.argv[1], "r") as bitsrc:
			data = BITalinoData(bitsrc.read())
			print data.toJson()
	except IndexError as e:
		print "Missing BITalino data file argument"

if __name__ == '__main__':
    main()
