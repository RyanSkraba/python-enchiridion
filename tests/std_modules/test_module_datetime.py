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
import datetime
import unittest

"""
Unit tests demonstrating python datetime.

https://docs.python.org/3/library/datetime.html
"""


class DatetimeModuleTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_basic(self) -> None:
        my_date = datetime.datetime.strptime("2011/06/13", "%Y/%m/%d")
        self.assertEqual(datetime.datetime(2011, 6, 13, 0, 0), my_date)
        my_date2 = datetime.datetime.strptime("2015/09/19", "%Y/%m/%d")
        interval = (my_date2 - my_date).days
        self.assertEqual(1559, interval)
        my_date3 = my_date2 + datetime.timedelta(days=interval)
        self.assertEqual("2019/12/26", my_date3.strftime("%Y/%m/%d"))


if __name__ == "__main__":
    unittest.main()
