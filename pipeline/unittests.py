#! /usr/bin/env python
"""
Unit tests
"""

import unittest
import parser
import os

class test_pipeline(unittest.TestCase):
    LEN_FULL_DATETIME = 26
    LEN_TEST_FILE = 727

    def setUp(self):
        try:
            __location__ = os.path.realpath(
                os.path.join(os.getcwd(), os.path.dirname(__file__)))
            self.src = open(os.path.join(__location__, "bit-test-data.txt"))
            self.badFreq = open(os.path.join(__location__, "bad-frequency.txt"))
            self.badStartTime = open(os.path.join(__location__, "bad-starttime.txt"))
        except:
            print "Error during unittest setup"

    def test_open(self):
        self.assertEquals(len(self.src.read().split("\n")), 20)

    def test_parser(self):
        bitdo = parser.BITdo(self.src)
        self.assertEquals(len(bitdo.toJson()), test_pipeline.LEN_TEST_FILE)
        self.assertTrue(len(bitdo.channels), 5)
        self.assertEquals(bitdo.header["SamplingFrequency"], "1000")
        self.assertEquals(len(bitdo.channels[4]["data"]), 16)
        # Assure that datetime is to microsecond precision
        self.assertEquals(len(bitdo.header["StartDateTime"]), test_pipeline.LEN_FULL_DATETIME)

    def test_parser_errors(self):
        self.assertRaises(AttributeError, parser.BITdo, (self.badFreq))
        self.assertRaises(AttributeError, parser.BITdo, (self.badStartTime))

if __name__ == '__main__':
    unittest.main()
