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

import unittest
import re

"""
Unit tests demonstrating regular expression operations.

https://docs.python.org/3/library/re.html
"""


class ReModuleTestSuite(unittest.TestCase):

    def test_basic(self) -> None:
        # Precompile a pattern
        regex = re.compile("ab*c")
        self.assertIsInstance(regex, re.Pattern)
        # Match (from the beginning) successfully
        result = regex.match("abbbcd")
        self.assertIsInstance(result, re.Match)
        self.assertTrue(result)
        # No match
        result = regex.match("xac")
        self.assertIsNone(result)
        # Module-level functions without compiling the pattern first
        self.assertTrue(re.match("ab*c", "abbcd"))
        self.assertFalse(re.match("ab*c", "xac"))

    def test_match(self) -> None:
        """A Match object is returned by the match function."""
        regex = re.compile("a(b*)(c*)d")
        # Group or __getitem__ are used to fetch groups
        result = regex.match("ade")
        self.assertEqual(result[0], "ad")
        self.assertEqual(result[1], "")
        self.assertEqual(result[2], "")
        self.assertEqual(result.lastindex, 2)

        # You can get the information used to create the match
        self.assertEqual(result.pos, 0)
        self.assertEqual(result.endpos, 3)
        self.assertEqual(result.re, regex)
        self.assertEqual(result.string, "ade")

        result = regex.match("abbbccd")
        self.assertEqual(result[0], "abbbccd")
        self.assertEqual(result[1], "bbb")
        self.assertEqual(result[2], "cc")
        self.assertEqual(result.lastindex, 2)
        self.assertEqual(result.expand(r"\2 \1"), "cc bbb")

    def test_search_match_fullmatch(self) -> None:
        regex = re.compile("a.c")

        # Search, match and fullmatch are for anywhere, the start and the whole string respectively
        self.assertEqual(regex.search("xyzabczyx").group(0), "abc")
        self.assertIsNone(regex.match("xyzabczyx"))
        self.assertIsNone(regex.fullmatch("xyzabczyx"))

        self.assertEqual(regex.search("abczyx").group(0), "abc")
        self.assertEqual(regex.match("abczyx").group(0), "abc")
        self.assertIsNone(regex.fullmatch("abczyx"))

        self.assertEqual(regex.search("abc").group(0), "abc")
        self.assertEqual(regex.match("abc").group(0), "abc")
        self.assertEqual(regex.fullmatch("abc").group(0), "abc")

        # This could be clarified with regex start and end markers
        regex = re.compile("^x.z$")

        self.assertIsNone(regex.search("xyzaaa"))
        self.assertIsNone(regex.match("xyzaaa"))
        self.assertIsNone(regex.fullmatch("xyzaaa"))

        self.assertEqual(regex.search("xyz").group(0), "xyz")
        self.assertEqual(regex.match("xyz").group(0), "xyz")
        self.assertEqual(regex.fullmatch("xyz").group(0), "xyz")

    def test_pos_endpos(self) -> None:
        regex = re.compile("a{3,}c")

        # Search, match and fullmatch are for anywhere, the start and the whole string respectively
        self.assertEqual(regex.search("xaaaaaczyx", pos=0).group(0), "aaaaac")
        self.assertEqual(regex.search("xaaaaaczyx", pos=1).group(0), "aaaaac")
        self.assertEqual(regex.search("xaaaaaczyx", pos=2).group(0), "aaaac")
        self.assertEqual(regex.search("xaaaaaczyx", pos=3).group(0), "aaac")
        self.assertIsNone(regex.search("xaaaaaczyx", pos=4))
        self.assertEqual(regex.search("xaaaaaczyx", pos=1, endpos=8).group(0), "aaaaac")
        self.assertEqual(regex.search("xaaaaaczyx", pos=2, endpos=7).group(0), "aaaac")
        self.assertIsNone(regex.search("xaaaaaczyx", pos=2, endpos=6))

        # Note that start markers don't match positions!
        regex = re.compile("^a{3,}c+$")
        self.assertEqual(regex.search("aaaaacc", pos=0, endpos=7).group(0), "aaaaacc")
        self.assertIsNone(regex.search("aaaaacc", pos=1))
        # But end markers do.
        self.assertEqual(regex.search("aaaaacc", pos=0, endpos=6).group(0), "aaaaac")

    def test_replace(self) -> None:
        out = re.sub("\\bPORJ-(\\d+)", "PROJ-\\1", "Please fix PORJ-986 first")
        self.assertEqual(out, "Please fix PROJ-986 first")


if __name__ == "__main__":
    unittest.main()
