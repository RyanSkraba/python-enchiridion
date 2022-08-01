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
import packaging.version


class AvroModuleTestSuite(unittest.TestCase):
    """Test cases for Apache Avro https://avro.apache.org"""

    avro_version = packaging.version.parse(avro.__version__)

    def test_avro3182(self) -> None:
        # These are all fine
        schema = avro.schema.parse('"string"')
        self.assertEqual(schema.type, "string")
        schema = avro.schema.parse('{"type": "string"}')
        self.assertEqual(schema.type, "string")
        schema = avro.schema.parse('["null", "string"]')
        self.assertEqual(schema.type, "union")

        # But this is invalid
        with self.assertRaises(avro.errors.SchemaParseException) as ex:
            avro.schema.parse('{"type": ["null", "string"]}')
        self.assertEqual(str(ex.exception), "Undefined type: ['null', 'string']")

    def test_names(self) -> None:
        # This is an invalid type name for all versions of Avro
        with self.assertRaises(avro.errors.SchemaParseException) as ex:
            avro.schema.parse('{"type": "record", "name": "int", "fields": []}')
        self.assertEqual(str(ex.exception), "int is a reserved type name.")

        # This is invalid in Avro 1.11.0 but valid in Avro 1.11.1
        if AvroModuleTestSuite.avro_version <= packaging.version.parse("1.11.0"):
            with self.assertRaises(avro.errors.SchemaParseException) as ex:
                avro.schema.parse('{"type": "record", "name": "record", "fields": []}')
            self.assertEqual(str(ex.exception), "record is a reserved type name.")


if __name__ == "__main__":
    unittest.main()
