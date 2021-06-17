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
import logging
import unittest
import warnings


class UnittestModuleTestSuite(unittest.TestCase):
    def test_asserts(self):
        self.assertEqual(2, 1 + 1)
        self.assertNotEqual(1, 1 + 1)

        self.assertAlmostEqual(0.99999999, 1)
        self.assertAlmostEqual(1.0, 1.001, places=2)
        self.assertAlmostEqual(1.0, 1.25, delta=0.3)

        self.assertNotAlmostEqual(0.9999999, 1)
        self.assertNotAlmostEqual(1.0, 1.01, places=2)
        self.assertNotAlmostEqual(1.0, 1.35, delta=0.3)

        self.assertSequenceEqual([1, 2], (1, 1 + 1))
        self.assertListEqual([1, 2], [1, 1 + 1])
        self.assertTupleEqual((1, 2), (1, 1 + 1))
        self.assertSetEqual({1, 2}, {2, 1})

        self.assertIn(1, {1, 2})
        self.assertNotIn(2, {1, 3})
        self.assertIs(2, 1 + 1)
        self.assertIsNot(1, 1 + 1)
        self.assertDictEqual({"id": 2}, {"id": 1 + 1})
        self.assertCountEqual([1, 2, 2, 3], [3, 2, 1, 2])

        self.assertMultiLineEqual("A\nB", "A\nB")

        self.assertLess(1, 2)
        self.assertLessEqual(1, 1)
        self.assertGreater(2, 1)
        self.assertGreaterEqual(1, 1)

        self.assertIsNone(None)
        self.assertIsNotNone(1)

        self.assertIsInstance(self, unittest.TestCase)
        self.assertNotIsInstance(self, unittest.SkipTest)

        self.assertRegex("unittest", "itte")
        self.assertNotRegex("unittest", "utte")

    def test_raises(self):
        with self.assertRaises(Exception):
            raise Exception("ERROR!!!")

        with self.assertRaises(Exception) as cm:
            raise Exception("ERROR!!!")
        self.assertEqual(str(cm.exception), "ERROR!!!")

        with self.assertRaisesRegex(Exception, "RRO"):
            raise Exception("ERROR!!!")

        with self.assertWarns(Warning):
            warnings.warn("WARNING!!")

        with self.assertWarnsRegex(Warning, "WARNING"):
            warnings.warn("WARNING!!")

    def test_logger(self):

        with self.assertLogs("unittest", level="INFO") as cm:
            logging.getLogger("unittest").info("INFO!")
            logging.getLogger("unittest.x").error("ERROR!!!")
        self.assertEqual(
            cm.output, ["INFO:unittest:INFO!", "ERROR:unittest.x:ERROR!!!"]
        )


if __name__ == "__main__":
    unittest.main()
