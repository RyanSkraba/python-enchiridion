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

import avro.schema


class AvroModuleTestSuite(unittest.TestCase):
    """Test cases for Apache Avro http://avro.apache.org"""

    def test_avro3182(self) -> None:

        # These are all fine
        schema = avro.schema.parse('"string"')
        self.assertEqual(schema.type, "string")
        schema = avro.schema.parse('{"type": "string"}')
        self.assertEqual(schema.type, "string")
        schema = avro.schema.parse('["null", "string"]')
        self.assertEqual(schema.type, "union")

        # But this is invalid
        with self.assertRaises(avro.schema.SchemaParseException) as ex:
            avro.schema.parse('{"type": ["null", "string"]}')
        self.assertEqual(str(ex.exception), "Undefined type: ['null', 'string']")


if __name__ == "__main__":
    unittest.main()
