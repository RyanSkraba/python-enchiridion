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
import packaging.version
import avro


class PackagingModuleTestSuite(unittest.TestCase):
    def test_avro_version(self) -> None:
        avro_version = packaging.version.parse(avro.__version__)
        self.assertEqual(avro_version.major, 1)
        self.assertEqual(avro_version.minor, 11)
        self.assertEqual(avro_version.micro, 1)

    def test_version(self) -> None:
        # Comparing by string isn't the right thing to do for versions
        self.assertGreater("1.9.1", "1.10.1")
        self.assertLess(
            packaging.version.parse("1.9.1"), packaging.version.parse("1.10.1")
        )
        self.assertLess(
            packaging.version.parse("1.9.1"), packaging.version.parse("1.9.2")
        )
        self.assertLess(
            packaging.version.parse("1.9.1"), packaging.version.parse("2.0.0")
        )


if __name__ == "__main__":
    unittest.main()
