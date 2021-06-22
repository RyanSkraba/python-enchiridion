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


if __name__ == "__main__":
    unittest.main()
