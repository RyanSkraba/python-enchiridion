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
import uuid

"""
Unit tests demonstrating UUID objects according to RFC 4122.

https://docs.python.org/3/library/uuid.html
"""


class UuidModuleTestSuite(unittest.TestCase):
    def test_match(self) -> None:
        id = uuid.UUID("12345678-1234-5678-1234-567812345678")
        self.assertEqual(str(id), "12345678-1234-5678-1234-567812345678")
        id2 = uuid.UUID(str(id))
        self.assertEqual(id, id2)


if __name__ == "__main__":
    unittest.main()
