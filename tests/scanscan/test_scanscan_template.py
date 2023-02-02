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

import os.path
import tempfile
import unittest
from pathlib import Path

from scanscan.ScanScanTemplate import ScanScanTemplate


class ScanScanTemplateTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_basic(self):
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            dtmp = Path(tmp_dir_name)

            with open(dtmp / "test.template", "w") as f:
                f.write("{{name}}\n\n{{name}}\n---\n")
            with open(dtmp / "test.input", "w") as f:
                f.write("one\ntwo\nthree\nfour\nfive\nsix\nseven\n")

            tmpl = ScanScanTemplate(
                dtmp / "test.template", str(dtmp / "test.output%s.txt")
            )
            with open(dtmp / "test.input", "r") as infile:
                tmpl.apply_input(infile)
            tmpl.write()

            self.assertTrue(os.path.exists(dtmp / "test.output1.txt"))
            self.assertTrue(os.path.exists(dtmp / "test.output2.txt"))
            self.assertTrue(os.path.exists(dtmp / "test.output3.txt"))
            self.assertTrue(os.path.exists(dtmp / "test.output4.txt"))


if __name__ == "__main__":
    unittest.main()
