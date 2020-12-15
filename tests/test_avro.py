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

import io
import unittest

import avro.io
import avro.schema
import avro.timezones


def write_datum(datum, writers_schema):
    writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(writer)
    datum_writer = avro.io.DatumWriter(writers_schema)
    datum_writer.write(datum, encoder)
    return writer, encoder, datum_writer


def read_datum(buffer, writers_schema, readers_schema=None):
    reader = io.BytesIO(buffer)
    decoder = avro.io.BinaryDecoder(reader)
    datum_reader = avro.io.DatumReader(writers_schema, readers_schema)
    return datum_reader.read(decoder)


class AvroModuleTestSuite(unittest.TestCase):
    def test_record(self):
        writers_schema = avro.schema.parse(
            """
                {
                  "type" : "record",
                  "name" : "SimpleRecord",
                  "doc" : "Simple two column record",
                  "fields" : [ {
                    "name" : "id",
                    "type" : "long"
                  }, {
                    "name" : "name",
                    "type" : "string"
                  } ]
                }"""
        )
        datum = {"id": 1, "name": "one"}
        writer, encoder, datum_writer = write_datum(datum, writers_schema)
        buffer = writer.getvalue()
        self.assertEqual(len(buffer), 5)
        round_trip_datum = read_datum(buffer, writers_schema)
        self.assertEqual(round_trip_datum, {"id": 1, "name": "one"})


if __name__ == "__main__":
    unittest.main()
