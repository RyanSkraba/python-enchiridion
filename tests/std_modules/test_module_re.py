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
        regex = re.compile("ab*c")

        # matches the beginning of the string.
        result = regex.match("abbbc")
        self.assertEqual(result.pos, 0)
        result = regex.match("axxxc")
        self.assertIsNone(result)
        result = regex.match("acxxx")
        self.assertEqual(result.pos, 0)
        result = regex.match("xxxacxxx")
        self.assertIsNone(result)

    def test_replace(self) -> None:
        out = re.sub("\\bPORJ-(\\d+)", "PROJ-\\1", "Please fix PORJ-986 first")
        self.assertEqual(out, "Please fix PROJ-986 first")


if __name__ == "__main__":
    unittest.main()
