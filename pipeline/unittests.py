#! /usr/bin/env python

import unittest
import parser

class test_parser:
    def setUp(self):
        self.bitdo = 


    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)

if __name__ == '__main__':
	unittest.main()
