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


class A(object):
    def __init__(self, a="a1"):
        self.a = a


class B(A):
    def __init__(self, a="a2", b="b1"):
        super(B, self).__init__(a)
        self.b = b


class Basic(object):
    """A basic class with instance and class attributes and methods."""

    # A class attribute, accessed as self.d or Basic.d
    d = "Dd"

    def __init__(self, a="Aa", b="Bb"):
        """Constructor."""
        super(Basic, self).__init__()
        # Instance attributes, accessed only as self.a, etc.
        self.a = a
        self.b = b
        self.c = "Cc"

    def a_lower(self):
        return self.a.lower()

    def b_upper(self):
        return self.b.upper()

    @staticmethod
    def d_lower():
        return Basic.d.lower()


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
        self.assertEqual(test.d_lower(), "dd")

        # The class method
        self.assertEqual(Basic.d, "Dd")
        Basic.d = "Dd" * 10
        self.assertEqual(test.d, "DdDdDdDdDdDdDdDdDdDd")
        self.assertEqual(Basic.d, "DdDdDdDdDdDdDdDdDdDd")
        self.assertEqual(test.d_lower(), "dddddddddddddddddddd")
        self.assertEqual(Basic.d_lower(), "dddddddddddddddddddd")

        # A new instance
        test = Basic("AaAaAa", "BbBb")
        self.assertEqual(test.a, "AaAaAa")
        self.assertEqual(test.b, "BbBb")
        self.assertEqual(test.c, "Cc")
        self.assertEqual(test.d, "DdDdDdDdDdDdDdDdDdDd")
        self.assertEqual(test.a_lower(), "aaaaaa")
        self.assertEqual(test.b_upper(), "BBBB")
        self.assertEqual(test.d_lower(), "dddddddddddddddddddd")
        self.assertEqual(test.d_upper(), "DDDDDDDDDDDDDDDDDDDD")

    def testInheritance(self):
        a = A()
        b = B()
        self.assertEqual(a.a, "a1")
        self.assertEqual(b.a, "a2")
        self.assertEqual(b.b, "b1")
        self.assertIsInstance(a, A)
        self.assertNotIsInstance(a, B)
        self.assertIsInstance(b, A)
        self.assertIsInstance(b, B)
        self.assertTrue(isinstance(a, A))
        self.assertFalse(isinstance(a, B))
        self.assertTrue(isinstance(b, A))
        self.assertTrue(isinstance(b, B))


if __name__ == "__main__":
    unittest.main()
