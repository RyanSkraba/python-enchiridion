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


"""Successively apply content transformations to a file."""

from scanscan import ScanScan

import re


class ScanScanFile(ScanScan):

    """Successively apply content transformations to a file."""

    def __init__(self, filename):
        """Create the instance of this object from a file."""
        super(ScanScanFile, self).__init__()
        self.filename = filename
        self.load(filename)

    def load(self, filename):
        """Reload the contents of the specified file into memory."""
        with open(filename, "r") as content_file:
            self.content = content_file.read()

    def apply(self, content_lambda, die_on_not_applied=False):
        """Rewrite the stored content using the function.

        Keyword arguments:
        content_lambda -- a function to apply on the content of a file.
        """
        content = content_lambda(self.content)
        if content is not None:
            self.content = content
        elif die_on_not_applied:
            raise Exception("Not applied.")
        return self

    def contains_xml_comment(self, comment):
        """Return true if an xml comment exists with the exact content."""
        return re.search(r"\<!--\s*%s\s*--\>" % comment, self.content) is not None

    def write(self):
        """Write any modifications to this file."""
        with open(self.filename, "w") as content_file:
            content_file.write(self.content)
        return self
