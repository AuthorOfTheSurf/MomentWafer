#! /usr/bin/env python
"""
Unit tests
"""

import unittest
import parser
import os

class test_pipeline(unittest.TestCase):

    def setUp(self):
    	try:
    		self.src = open("../test/data/bit-test-data.txt")
    	except:
    		print "Error during unittest setup"

    def test_open(self):
        self.assertEquals(len(self.src.read().split("\n")), 20)

    def test_parser(self):
        bitdo = parser.BITdo(self.src)
        self.assertEquals(len(bitdo.toJson()), 717)
        self.assertTrue(len(bitdo.channels), 5)
        self.assertEquals(bitdo.header["SamplingFrequency"], "1000")
        self.assertEquals(len(bitdo.channels[4]["data"]), 16)

if __name__ == '__main__':
	unittest.main()
