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
"""Utility module for searching and replacing across files."""

import os
import re
from typing import Pattern

"""Utility for finding, searching and replacing in files."""


class ScanScan(object):

    """Utility for finding, searching and replacing in files."""

    # A regex for finding the first non numeric (version) tag in a file.
    fetch_tag: Pattern[str] = re.compile(r"^(.*?)([.-]\d+[.-]\d+[.-])")

    @staticmethod
    def apply_recursive(
        dir, content_lambda, file_lambda=None, die_on_not_applied=False
    ):
        """Scan a given directory to rewrite file content.

        Keyword arguments:
        dir -- the directory to recursively seach
        content_lambda -- a function to apply on the text of a file, returning
            the new text.
        file_lambda -- optional, a function to apply on the path and filename
            returning true if the file should be processed.
        """
        for root, dirs, files in os.walk(dir):
            for fn in files:
                if file_lambda is not None and not file_lambda(root, fn):
                    continue
                # logging:
                # print(fn)
                content = None
                with open(os.path.join(root, fn), "r") as content_file:
                    content = content_file.read()
                content = content_lambda(content)
                if content:
                    with open(os.path.join(root, fn), "w") as content_file:
                        content_file.write(content)
                elif die_on_not_applied:
                    raise Exception("Not applied on %s" % fn)

    @staticmethod
    def get_tag(filename):
        """Return the 'tag' portion of the filename (exclude version info).

        The version info is anything that matches .00.00 and the tag is any
        text that precedes it.  The separator can be a -.

        If there is no version, the entire filename is the tag.

        xyz-0.1.2.jar, xyz-0.1test.jar, xyz.0.1.2-test.jar => xyz
        xyz0.0.0.jar => xyz0.0.0.jar
        xyz0.0.jar => xyz0.0.jar
        xyz0.jar => xyz0.jar
        """
        match = ScanScan.fetch_tag.search(filename)
        return filename if match is None else match.group(1)

    @staticmethod
    def content_test_and_add_next(test, to_add):
        """Return a lambda that checks if a "test" line exists before adding.

        If the test line doesn't exist, it's skipped.  If it exists, and is
        not *already* followed by the desired subsequent line, the line is
        added.  If it is already followed, nothing changes.
        """

        def content_test_and_add_next_method(input):
            test_pattern = (
                r"(?P<test>(?P<space>[ \t]*)%s\s*?)\n" r"((?P<next>.*)\n)?" % test
            )
            match = re.search(test_pattern, input)
            if not match:
                return None
            test_line = match.group("test")
            actual_next_line = match.group("next")
            desired_next_line = re.sub(test, to_add, test_line)
            if actual_next_line == desired_next_line:
                return None
            dupl_pattern = "%s\n%s\n%s\n" % (
                test_line,
                desired_next_line,
                actual_next_line,
            )
            return re.sub(test_pattern, dupl_pattern, input)

        return content_test_and_add_next_method

    @staticmethod
    def content_test_and_add_prev(test, to_add):
        """Return a lambda that checks if a "test" line exists before adding.

        If the test line doesn't exist, it's skipped.  If it exists, and is
        not *already* followed by the desired subsequent line, the line is
        added.  If it is already followed, nothing changes.
        """

        def content_test_and_add_prev_method(input):
            test_pattern = (
                r"((?P<prev>.*)\n)?" r"(?P<test>(?P<space>[ \t]*)%s\s*?)\n" % test
            )
            match = re.search(test_pattern, input)
            if not match:
                return None
            test_line = match.group("test")
            actual_prev_line = match.group("prev")
            desired_prev_line = re.sub(test, to_add, test_line)
            if actual_prev_line == desired_prev_line:
                return None
            dupl_pattern = "%s\n%s\n%s\n" % (
                actual_prev_line,
                desired_prev_line,
                test_line,
            )
            return re.sub(test_pattern, dupl_pattern, input)

        return content_test_and_add_prev_method

    @staticmethod
    def content_replace(search, replace):
        """Simple re search and replace."""
        return lambda input: re.sub(search, replace, input)

    @staticmethod
    def content_replace_xml_by_comment_delimiter(comment, replacement):
        """Replace a XML commented section.

        All content between the <!-- comment --> and the NEXT comment is
        replaced.

        Keyword arguments:
        comment -- A constant string to search for in comments.
        replacement -- The replacement text to insert after the command and
            before the next comment.
        """

        def content_replace_xml_by_comment_delimiter_method(input):
            match = re.compile(
                r"""(?P<comment>\n[ \t]*<!--\s*%s\s*-->)
                (?P<to_replace>.*?)
                (?P<next_comment>[^\n]*<!--)
                """
                % re.sub(r"\s+", r"\\s+", re.sub(r"\s", r"\s", comment)),
                re.VERBOSE | re.MULTILINE | re.DOTALL,
            )
            return match.sub(r"\g<comment>\n%s\g<next_comment>" % replacement, input)

        return content_replace_xml_by_comment_delimiter_method

    @staticmethod
    def file_endswith(extension, include=None, exclude=None):
        """Return lambda that tests whether a filename matches an extension.

        Keyword arguments:
        extension -- a string that must match the end of the file.
        include - optional, a string that must be present in the filename.
        exclude - optional, a string that must not be present in the filename.
        """
        return (
            lambda dir, filename: filename.endswith(extension)
            and (include is None or include in filename)
            and (exclude is None or exclude not in filename)
        )

    @staticmethod
    def file_has_tag(tag, extension=None, include=None, exclude=None):
        """Return lambda that tests whether a filename matches a tag.

        Keyword arguments:
        tag -- the tag for the file (see ScanScan.get_tag).
        extension - optional, a string that must match the end of the file.
        include - optional, a string that must be present in the filename.
        exclude - optional, a string that must not be present in the filename.
        """
        return (
            lambda dir, filename: tag == ScanScan.get_tag(filename)
            and (extension is None or filename.endswith(extension))
            and (include is None or include in filename)
            and (exclude is None or exclude not in filename)
        )


class ScanScanError(Exception):

    """Exception from ScanScan."""

    def __init__(self, value):
        """Initialize the error with a value."""
        self.value = value

    def __str__(self):
        """Me as a string."""
        return repr(self.value)


if __name__ == "__main__":
    pass
