#! /usr/bin/env python
"""
Unit tests
"""

import unittest
import os
import parser
import aggregator
from service import WaferService
from py2neo import Graph
from py2neo import Node, Relationship
import requests


class test_pipeline(unittest.TestCase):
    LEN_DATETIME = 26
    LEN_TEST_FILE = 632

    def setUp(self):
        try:
            __location__ = os.path.realpath(
                os.path.join(os.getcwd(), os.path.dirname(__file__)))
            self.src = open(
                os.path.join(__location__, "data/bit-test-data.txt"))
            self.badFreq = open(
                os.path.join(__location__, "data/bad-frequency.txt"))
            self.badStartTime = open(
                os.path.join(__location__, "data/bad-starttime.txt"))
            self.graph = Graph("http://localhost:8484/db/data")
            self.graph.delete_all()
            self.service = WaferService(self.graph)
        except:
            print "Error during unittest setup"

    def tearDown(self):
        self.graph.delete_all()

    #
    # File tests
    #
    def test_open(self):
        self.assertEquals(len(self.src.read().split("\n")), 20)

    #
    # Parser tests
    #
    def test_parser(self):
        bitdo = parser.BITdo(self.src)
        self.assertEquals(len(bitdo.toJson()), test_pipeline.LEN_TEST_FILE)
        self.assertEquals(len(bitdo.channels.keys()), 5)
        self.assertEquals(bitdo.header["SamplingFrequency"], "1000")
        self.assertEquals(len(bitdo.channels["EMG"]), 16)
        # Assure that datetime is to microsecond precision
        self.assertEquals(
            len(bitdo.header["StartDateTime"]), test_pipeline.LEN_DATETIME)

    def test_parser_errors(self):
        self.assertRaises(AttributeError, parser.BITdo, (self.badFreq))
        self.assertRaises(AttributeError, parser.BITdo, (self.badStartTime))

    #
    # Aggregator tests
    #
    def test_aggregator_nums(self):
        a = [0, 0, 1, 1, 1]
        s = aggregator.streaksIn(a)
        self.assertEquals(s[0].getStreaks(), [2])
        self.assertEquals(s[0].getStreakExp(2), [4])
        self.assertEquals(s[1].getStreaks(), [3])
        self.assertEquals(s[1].getStreakExp(2), [9])

    def test_aggregator_bools(self):
        b = [True, False, False, True, False]
        s = aggregator.streaksIn(b)
        self.assertEquals(s[True].getStreaks(), [1, 1])
        self.assertEquals(s[False].getStreaks(), [2, 1])
        self.assertEquals(s[False].getStreakExp(2), [4, 1])

    def test_aggregator_strings(self):
        c = ["cat", "826", "826", "826", "~~", "~~", "cat", "cat", "~~"]
        s = aggregator.streaksIn(c)
        self.assertEquals(s["cat"].getStreaks(), [1, 2])
        self.assertEquals(s["cat"].getStreakExp(2), [1, 4])
        self.assertEquals(s["826"].getStreaks(), [3])
        self.assertEquals(s["826"].getStreakExp(3), [27])
        self.assertEquals(s["~~"].getStreaks(), [2, 1])
        self.assertEquals(s["~~"].getStreakExp(-1), [0.5, 1])

    def test_aggregator_average(self):
        bitdo = parser.BITdo(self.src)
        self.assertEquals(aggregator.average(bitdo.channels['EMG']), 525.4375)
        self.assertEquals(aggregator.average([1, 2, 3]), 2)
        self.assertEquals(aggregator.average([x for x in range(1000)]), 499.5)

    #
    # Annotator
    #
    def test_add_new_user(self):
        user = self.service.add_user("Duke")
        activity = self.service.add_activity(
            user, "Free Throws", "no description")
        self.service.add_moment(activity)
        self.service.add_moment(activity)
        self.assertEquals(count(self.graph.find("User")), 1)
        self.assertEquals(count(self.graph.find("Activity")), 1)
        self.assertEquals(count(self.graph.find("Moment")), 2)
        self.assertEquals(count(self.graph.find("Annotation")), 2)

    #
    # Graph API
    #
    def test_post_user(self):
        r = requests.post('http://localhost:8000/users', {
            'userid': 'AwesomeName'})
        self.assertEquals(r.status_code, 200)
        r = requests.post('http://localhost:8000/users', {})
        self.assertEquals(r.status_code, 400)

def count(iter):
    try:
        return len(iter)
    except TypeError:
        return sum(1 for _ in iter)

if __name__ == '__main__':
    unittest.main()
