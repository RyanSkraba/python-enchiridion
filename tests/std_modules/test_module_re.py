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
        """Finds a match at the beginning of the string."""
        regex = re.compile("a(b*)(c*)d")

        result = regex.match("ade")
        self.assertEqual(result[0], "ad")
        self.assertEqual(result[1], "")
        self.assertEqual(result[2], "")
        self.assertEqual(result.lastindex, 2)

        # Get the info used to create this match
        self.assertEqual(result.pos, 0)
        self.assertEqual(result.endpos, 3)
        self.assertEqual(result.re, regex)
        self.assertEqual(result.string, "ade")

        result = regex.match("abbbcde")
        self.assertEqual(result[0], "abbbcd")
        self.assertEqual(result[1], "bbb")
        self.assertEqual(result[2], "c")
        self.assertEqual(result.lastindex, 2)

    def test_search_match_fullmatch(self) -> None:
        regex = re.compile("a(b*)(c*)d")

        # Search, match and fullmatch are for anywhere, the start and the whole string respectively
        self.assertEqual(regex.search("xyzabbdzyx").group(0), "abbd")
        self.assertIsNone(regex.match("xyzabbdzyx"))
        self.assertIsNone(regex.fullmatch("xyzabbdzyx"))

        self.assertEqual(regex.search("abbdzyx").group(0), "abbd")
        self.assertEqual(regex.match("abbdzyx").group(0), "abbd")
        self.assertIsNone(regex.fullmatch("abbdzyx"))

        self.assertEqual(regex.search("abbd").group(0), "abbd")
        self.assertEqual(regex.match("abbd").group(0), "abbd")
        self.assertEqual(regex.fullmatch("abbd").group(0), "abbd")

        # This could be clarified with regex start and end markers
        regex = re.compile("^a(b*)(c*)d$")

        self.assertIsNone(regex.search("accdzyx"))
        self.assertIsNone(regex.match("accdzyx"))
        self.assertIsNone(regex.fullmatch("accdzyx"))

        self.assertEqual(regex.search("accd").group(0), "accd")
        self.assertEqual(regex.match("accd").group(0), "accd")
        self.assertEqual(regex.fullmatch("accd").group(0), "accd")

    def test_replace(self) -> None:
        out = re.sub("\\bPORJ-(\\d+)", "PROJ-\\1", "Please fix PORJ-986 first")
        self.assertEqual(out, "Please fix PROJ-986 first")


if __name__ == "__main__":
    unittest.main()
