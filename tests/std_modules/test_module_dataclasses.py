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
from dataclasses import dataclass
import unittest

"""
Unit tests demonstrating python data classes.

https://docs.python.org/3/library/dataclasses.html
"""


@dataclass
class SimpleRecord:
    """An id and a name."""

    name: str
    id: int = 0


class DataclassesModuleTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_simple_record(self) -> None:
        record = SimpleRecord("one", 1)
        self.assertEqual(1, record.id)
        self.assertEqual("one", record.name)
        self.assertEqual("SimpleRecord(name='one', id=1)", record.__repr__())

        record0 = SimpleRecord("zero")
        self.assertEqual("SimpleRecord(name='zero', id=0)", record0.__repr__())


if __name__ == "__main__":
    unittest.main()
