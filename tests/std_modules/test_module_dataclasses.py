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
import dataclasses
from dataclasses import dataclass
import unittest

"""
Unit tests demonstrating python data classes.

https://docs.python.org/3/library/dataclasses.html
"""


@dataclass(order=True)
class IssueId:
    """An issue has a project identifier and a number"""

    prj: str
    num: int = 0

    def __str__(self):
        """A custom string representation for the class"""
        return f"{self.prj}-{self.num}"


class DataclassesModuleTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_issue_id(self) -> None:
        issue = IssueId("PRJ", 1)
        self.assertEqual("PRJ", issue.prj)
        self.assertEqual(1, issue.num)
        self.assertEqual("IssueId(prj='PRJ', num=1)", issue.__repr__())
        self.assertEqual(IssueId(num=1, prj="PRJ"), issue)

    def test_issue_id_str(self) -> None:
        issue = IssueId("PRJ", 123)
        self.assertEqual("PRJ-123", issue.__str__())
        self.assertEqual("PRJ-123", str(issue))

    def test_issue_id_with_default(self) -> None:
        issue = IssueId("PRJ")
        self.assertEqual("IssueId(prj='PRJ', num=0)", issue.__repr__())
        self.assertEqual(IssueId("PRJ", 0), issue)
        self.assertNotEqual(IssueId("PRJ", 1), issue)
        self.assertLess(IssueId("PRJ", -1), issue)

    def test_issue_id_with_modification(self) -> None:
        issue = IssueId("PRJ")
        self.assertEqual("IssueId(prj='PRJ', num=0)", issue.__repr__())
        issue.num = 999
        self.assertEqual("IssueId(prj='PRJ', num=999)", issue.__repr__())

    def test_issue_id_with_replace(self) -> None:
        issue = IssueId("PRJ")
        issue2 = dataclasses.replace(issue)
        self.assertEqual(issue, issue2)
        issue2.prj = "NEW"
        self.assertNotEqual(issue, issue2)
        issue3 = dataclasses.replace(issue2, num=1000)
        self.assertEqual(IssueId("NEW", 1000), issue3)


if __name__ == "__main__":
    unittest.main()
