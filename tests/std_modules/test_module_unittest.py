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
import sys
import unittest
import warnings

"""
Unit tests in Python
"""


class UnittestModuleAssertionsTestSuite(unittest.TestCase):
    """Test cases for assertions."""

    def test_asserts_equals(self) -> None:
        """Simple examples of equality assertions."""

        # Boolean expressions
        self.assertTrue(1 + 1 == 2)
        self.assertFalse(1 + 1 == 3)

        # Test for equality using `==` and `is`
        self.assertEqual(2, 1 + 1)
        self.assertNotEqual(1, 1 + 1)
        self.assertIs(2, 1 + 1)
        self.assertIsNot(1, 1 + 1)

        # Note that IntelliJ gives an error message: Expected 3, Actual 2
        with self.assertRaises(AssertionError) as cm:
            self.assertEquals(3, 1 + 1)
        self.assertEquals(str(cm.exception), "3 != 2")
        with self.assertRaises(AssertionError) as cm:
            self.assertIs(3, 1 + 1)
        self.assertEquals(str(cm.exception), "3 is not 2")

        # All of the asserts can have messages.
        self.assertIs(2, 1 + 1, msg="Basic arithmetic")

        with self.assertRaises(AssertionError) as cm:
            self.assertIs(3, 1 + 1, msg="Basic arithmetic")
        self.assertEquals(str(cm.exception), "3 is not 2 : Basic arithmetic")

    def test_asserts_floating_point(self) -> None:
        """Simple examples of floating point assertions."""

        # Floating point equality
        self.assertAlmostEqual(0.99999999, 1)
        self.assertAlmostEqual(1.0, 1.001, places=2)
        self.assertAlmostEqual(1.0, 1.25, delta=0.3)
        self.assertNotAlmostEqual(0.9999999, 1)
        self.assertNotAlmostEqual(1.0, 1.01, places=2)
        self.assertNotAlmostEqual(1.0, 1.35, delta=0.3)

    def test_asserts_collections(self) -> None:
        """Simple examples of collection assertions."""

        # Collections
        self.assertSequenceEqual([1, 2], (1, 1 + 1))
        self.assertListEqual([1, 2], [1, 1 + 1])
        self.assertTupleEqual((1, 2), (1, 1 + 1))
        self.assertSetEqual({1, 2}, {2, 1})

        self.assertIn(1, {1, 2})
        self.assertNotIn(2, {1, 3})
        self.assertDictEqual({"id": 2}, {"id": 1 + 1})
        self.assertCountEqual([1, 2, 2, 3], [3, 2, 1, 2])

    def test_asserts_others(self) -> None:
        """Simple examples of collection assertions."""

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

    def test_subtest(self) -> None:
        """Subtests can be used to parameterize tests."""
        for num in ["One", "Two", "Six", "Ten"]:
            with self.subTest(num=num):
                # Each success and failure is reported.
                self.assertEqual(3, len(num))


class UnittestModuleFailuresTestSuite(unittest.TestCase):
    """Test cases for exceptions and failures."""

    def test_raises(self) -> None:
        """Simple examples of collection assertions."""
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

    def test_logger(self) -> None:
        with self.assertLogs("unittest", level="INFO") as cm:
            logging.getLogger("unittest").info("INFO!")
            logging.getLogger("unittest.x").error("ERROR!!!")
        self.assertEqual(
            cm.output, ["INFO:unittest:INFO!", "ERROR:unittest.x:ERROR!!!"]
        )

    @unittest.expectedFailure
    def test_fail(self) -> None:
        self.fail("Always fails.")

    @unittest.expectedFailure
    def test_bad_assertion(self) -> None:
        self.assertEqual(3, 1 + 1)


def skipUnlessYes(confirmation: str = "No"):
    """A custom annotation that skips only if the confirmation is exactly 'Yes'"""
    if confirmation != "Yes":
        return lambda func: func
    return unittest.skip("Skip requested")


@unittest.skipIf(False, "You can annotate a TestSuite to skip.")
class UnittestModuleSkipTestSuite(unittest.TestCase):
    """Test cases for skipped tests."""

    class_running: bool = False

    def setUp(self) -> None:
        self.running = True

    def tearDown(self) -> None:
        self.running = False

    @classmethod
    def setUpClass(cls) -> None:
        cls.class_running = True

    @classmethod
    def tearDownClass(cls) -> None:
        cls.class_running = False

    @unittest.skip("Never run this test")
    def test_skip(self) -> None:
        self.fail("Skipped -- we shouldn't arrive here")

    @unittest.skipIf(sys.version_info.major > 1, "Only supported for python 1")
    def test_skip_if(self) -> None:
        self.fail("Skipped -- we shouldn't arrive here")

    @unittest.skipUnless(sys.platform.startswith("DubiOs"), "Requires specific OS")
    def test_skip_unless(self) -> None:
        self.fail("Skipped -- we shouldn't arrive here")

    def test_skip_internally(self) -> None:
        if self.running and self.class_running:
            self.skipTest("Skip when running")
        self.fail("Skipped -- we shouldn't arrive here")

    @skipUnlessYes("No")
    def test_not_custom_skipped(self) -> None:
        self.assertEqual(2, 1 + 1)

    @skipUnlessYes("Yes")
    def test_custom_skipped(self) -> None:
        self.assertEqual(3, 1 + 1)


if __name__ == "__main__":
    unittest.main()
