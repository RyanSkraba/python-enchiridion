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
import argparse
import unittest

"""
Unit tests demonstrating the parser for command-line options, arguments and sub-commands.

https://docs.python.org/3/library/argparse.html
"""


class ArgparseModuleTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_basic(self) -> None:
        """A basic example for parsing arguments"""
        parser = argparse.ArgumentParser(description="Process some integers.")
        parser.add_argument(
            "integers",
            metavar="N",
            type=int,
            nargs="+",
            help="an integer for the accumulator",
        )
        parser.add_argument(
            "--sum",
            dest="accumulate",
            action="store_const",
            const=sum,
            default=max,
            help="sum the integers (default: find the max)",
        )

        args = parser.parse_args(["--sum", "7", "-1", "42"])
        print(args.accumulate(args.integers))


if __name__ == "__main__":
    unittest.main()
