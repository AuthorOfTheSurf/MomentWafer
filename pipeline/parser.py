#! /usr/bin/env python
"""
Used to format the raw data text files produced by a BITalino
Parses the json-text format into a Python object more appropriate for
processing by the the MATL application

Sample BITalino txt file:

    # JSON Text File Format
    # {"SamplingResolution": "10", "SampledChannels": [1], "SamplingFrequency": "1000", "ColumnLabels": ["SeqN", "Digital0", "Digital1", "Digital2", "Digital3", "EMG"], "AcquiringDevice": "98:D3:31:XX:XX:XX", "Version": "111", "StartDateTime": "2015-2-2 10:30:2"}
    # EndOfHeader
    0   1   1   1   1   467 
    1   1   1   1   1   467 
    2   1   1   1   1   472 
    3   1   1   1   1   476 
    4   1   1   1   1   478 
    ...

"""

import sys
import json
import numpy

"""
BITalino data object, a plain old Python object
Accepts a BITalino .txt data file
- Header json into dict
- Parses colums into numpy arrays
"""
class BITdo:
    def __init__(self, BITalinoTxtData):
        next(BITalinoTxtData)
        self._header = json.loads(next(BITalinoTxtData)[2:])
        next(BITalinoTxtData)
        self._channels = self.makeChannels(BITalinoTxtData)
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
    See the description for BITdo.channels
    """
    def makeChannels(self, dataStream):
        channels = []
        labels = self._header["ColumnLabels"]
        # Each line has a trailing tab, newline, and carrage return. Datastream ends with a blank line
        fmtStream = [line[:-3].split("\t") for line in dataStream if len(line) > 0]
        na = numpy.array(fmtStream).astype(int)
        for col, label in enumerate(labels):
            channels.append({
                "data": na[:,col], # Each column of numpy.array becomes the channel's data
                "label": label # Also include label for the data
            }) if col != 0 else None
        return channels
    """
    Return a JSON representation of this BITdo object
    """
    def toJson(self):
        jsonCh = [{"label": ch["label"], "data": ch["data"].tolist()} for ch in self._channels]
        return json.dumps({ "header": self._header, "channels": jsonCh })

"""
Return a json representation of the supplied BITalino data .txt file
"""
def main():
    try:
        with open(sys.argv[1], "r") as bitsrc:
            data = BITdo(bitsrc)
            print data.toJson()
    except IndexError as e:
        print "Missing BITalino data file argument"

if __name__ == '__main__':
    main()
