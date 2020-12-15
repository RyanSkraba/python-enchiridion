#!/usr/bin/env python3
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


"""A simple mechanism to replace tags in a template with multiple values."""

from scanscan.ScanScanFile import ScanScanFile

import re


class ScanScanTemplate(ScanScanFile):

    """A simple mechanism to replace tags in a template with values."""

    def __init__(self, tmpl_filename, save_filename):
        """Create a template instance based on the given template name.

        tmpl_filename: the source of the template
        save_filename: the output file(s).  A %s will be replaced by an
            integer.
        """
        super(ScanScanTemplate, self).__init__(tmpl_filename)
        self.__tmpl_filename = tmpl_filename
        self.__save_filename = save_filename
        self.__count = 1

    def apply_input(self, input, tag="name"):
        r"""Replace all occurrences of {{tag}} by input values."""
        for line in input:
            original = self.content
            self.apply(lambda c: re.sub(r"{{" + tag + r"}}", line.rstrip(), c, 1))
            if original == self.content:
                self.write()
                self.apply(lambda c: re.sub(r"{{" + tag + r"}}", line.rstrip(), c, 1))

    def write(self):
        r"""Override the write to append an integer value to the filename."""
        self.filename = self.__save_filename % self.__count
        super(ScanScanTemplate, self).write()
        self.load(self.__tmpl_filename)
        self.__count = self.__count + 1
