# -*- mode: python -*-
# -*- coding: utf-8 -*-

##
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Object-oriented python notes.
"""
import unittest


class Basic(object):
    """A basic class with instance and class attributes and methods."""

    d = "Dd"

    def __init__(self, a="Aa", b="Bb"):
        """Constructor."""
        super(Basic, self).__init__()
        self.a = a
        self.b = b
        self.c = "Cc"

    def a_lower(self):
        return self.a.lower()

    def b_upper(self):
        return self.b.upper()


class BasicWithSlots(object):

    __slots__ = ["a", "b"]

    d = "D"

    def __init__(self, a="a", b="b"):
        """Constructor."""
        super(Basic, self).__init__()
        self.a = a
        self.b = b
        # self.c = "c" would fail


class BasicObjectTestSuite(unittest.TestCase):
    def testBasic(self):

        test = Basic()
        self.assertEqual(test.a, "Aa")
        self.assertEqual(test.b, "Bb")
        self.assertEqual(test.c, "Cc")
        self.assertEqual(test.d, "Dd")
        self.assertEqual(test.a_lower(), "aa")
        self.assertEqual(test.b_upper(), "BB")

        # The class method
        self.assertEqual(Basic.d, "Dd")
        Basic.d = "Dd" * 10
        self.assertEqual(Basic.d, "DdDdDdDdDdDdDdDdDdDd")

        # A new instance
        test = Basic("AaAaAa", "BbBb")
        self.assertEqual(test.a, "AaAaAa")
        self.assertEqual(test.b, "BbBb")
        self.assertEqual(test.c, "Cc")
        self.assertEqual(test.d, "DdDdDdDdDdDdDdDdDdDd")
        self.assertEqual(test.a_lower(), "aaaaaa")
        self.assertEqual(test.b_upper(), "BBBB")


if __name__ == "__main__":
    unittest.main()
