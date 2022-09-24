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
import logging

"""
Unit tests demonstrating the logging facility for Python.

https://docs.python.org/3/library/logging.html
"""


class LoggingModuleTestSuite(unittest.TestCase):
    def test_logging(self) -> None:
        """Using the module functions directly."""
        logging.debug("Something is happening: %s", "Argument")
        logging.info("Something is happening: %s", "Argument")
        logging.warning("Something is happening: %s", "Argument")
        logging.error("Something is happening: %s", "Argument")
        logging.critical("Something is happening: %s", "Argument")


if __name__ == "__main__":
    unittest.main()
