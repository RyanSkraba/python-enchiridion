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


"""
Learned from : http://docs.python.org/3.9/tutorial/introduction.html

Super simple lesson on the simplest types and operators.
"""
import unittest


class Tutorial3Introduction(unittest.TestCase):
    def testNumbers(self):
        """Operations on numbers."""

        # Integers
        self.assertEqual(5, 2 + 3, msg="addition")
        self.assertEqual(11, 2 + 3 * 3, msg="order of operations")
        self.assertEqual(15, (2 + 3) * 3, msg="order of operations")
        self.assertEqual(3, 19 // 5, msg="floor division")
        self.assertEqual(4, 19 % 5, msg="mod division")
        self.assertEqual(9, 3**2, msg="exponents")

        # Floating point
        self.assertEqual(3.8, 19 / 5, "division is always floating point")
        # Note it's a good practice to use almost equals on floats
        self.assertAlmostEqual(5.0, 2.0 + 3, msg="addition")
        self.assertAlmostEqual(3.8, 19.0 / 5, msg="division")
        self.assertAlmostEqual(0.25, 0.5**2, msg="exponents")
        self.assertAlmostEqual(1.41421356, 2**0.5, msg="seven decimal places")
        self.assertAlmostEqual(1.41, round(2**0.5, 2), msg="rounding")

    def testVariables(self):
        """Variable assignment."""
        a = 5
        self.assertEqual(5, a, msg="assignment")
        b = c = 5
        self.assertEqual(5, b, msg="multiple assignment")
        self.assertEqual(5, c, msg="multiple assignment")

    def testComplex(self):
        """Operations on complex numbers."""
        # probably not very interesting, but present
        # both parts are always float
        a = 3 + 4j
        self.assertAlmostEqual(5.0, abs(a), msg="magnitude")
        self.assertAlmostEqual(3.0, a.real, msg="real")
        self.assertAlmostEqual(4.0, a.imag, msg="imaginary")
        self.assertEqual(5 + 5j, a + (2 + 1j), msg="addition")

    def testStringFormats(self):
        # escaping rules
        self.assertEqual("Hello world", "Hello world", msg="quote types")
        self.assertEqual("How's it going?", "How's it going?", msg="escaped '")
        self.assertEqual('"Fine," he said.', '"Fine," he said.', msg='escaped "')
        self.assertEqual(
            '"You\'re sure?" she asked.', '"You\'re sure?" she asked.', msg="embedded"
        )

        # inernal backslashes takes out newlines, but retains whitespace
        actual = "Catch your thoughts and hold them tightly,\n\
  Let each one an honor be;\n\
Purge them, scourge them, burnish brightly,\n\
  Then in love set each one free."
        # equivalent form of backslash outside the quote to create the expected
        expected = (
            "Catch your thoughts and hold them tightly,\n  Let each one an "
            "honor be;\nPurge them, scourge them, burnish brightly,\n  Then in "
            "love set each one free."
        )
        self.assertEqual(expected, actual, msg="backslash extension")

        # triple quote preserves newlines
        actual = """\
Catch your thoughts and hold them tightly,
  Let each one an honor be;
Purge them, scourge them, burnish brightly,
  Then in love set each one free."""
        self.assertEqual(expected, actual, 'triple quote """')
        # The code beautifier will replace all '''

        # concatenate and repeated
        a = "word"
        self.assertEqual("worda", a + "a", "plus concat")
        self.assertEqual("wordwordword", a * 3, "repeat")
        # this concat can't be done with a variable or mutable obj
        self.assertEqual("worda", "word" "a", "close literal concat")

        # indexed and slices
        # characters are simply one letter strings
        word = a
        self.assertEqual("d", word[3])
        self.assertEqual("wo", word[0:2])
        self.assertEqual("rd", word[2:4])
        self.assertEqual("wo", word[:2])
        self.assertEqual("rd", word[2:])
        self.assertEqual("word", word[:])

        # invariant a[:i] + a[i:] == a, even if i is out of bounds
        for i in range(-1, 5):
            self.assertEqual("word", a[:i] + a[i:], "a[:" + str(i) + "] +...")

        # negative indexes are ok in slices
        self.assertEqual("or", word[1:3])
        self.assertEqual("or", word[-3:3])
        self.assertEqual("or", word[1:-1])
        self.assertEqual("or", word[-3:-1])
        self.assertEqual("wor", word[:-1])
        self.assertEqual("ord", word[-3:])

        # out of bound indexes are ok in slices (NOT in lookups)
        self.assertEqual("ord", word[1:1000])
        self.assertEqual("wor", word[-1000:3])

        # Strings are immutable : word[1] = "0" results in TypeError
        with self.assertRaises(TypeError):
            word[1] = 0

        # you can use a negative index in a lookup
        self.assertEqual("d", word[-1])
        self.assertEqual("r", word[-2])

        # But outside of a slice, a negative index must be valid
        with self.assertRaises(IndexError):
            word[-100]

        # and you can apply a len() function to get the size
        self.assertEqual(4, len(word))

        # raw strings with an r
        actual = (
            r"Catch your thoughts and hold them tightly,\n  Let each one an "
            r"honor be;"
        )
        expected = (
            "Catch your thoughts and hold them tightly,\\n  Let each one an honor be;"
        )
        self.assertEqual(expected, actual, "raw")

    def testLists(self):
        a = ["spam", "eggs", 100, 1234]
        self.assertEqual(a, ["spam", "eggs", 100, 1234])

        # Like string indices, list indices start at 0, and lists can be sliced,
        # concatenated and so on:
        self.assertEqual(a[0], "spam")
        self.assertEqual(a[3], 1234)
        self.assertEqual(a[-2], 100)
        self.assertEqual(a[1:-1], ["eggs", 100])
        self.assertEqual(a[:2] + ["bacon", 2 * 2], ["spam", "eggs", "bacon", 4])
        self.assertEqual(
            3 * a[:3] + ["Boo!"],
            ["spam", "eggs", 100, "spam", "eggs", 100, "spam", "eggs", 100, "Boo!"],
        )

        # All slice operations return a new list containing the requested elements.
        # This means that the following slice returns a shallow copy of the list a:
        self.assertEqual(a[:], ["spam", "eggs", 100, 1234])
        self.assertIsNot(a, a[:])
        # Unlike strings, which are immutable, it is possible to change individual
        # elements of a list:
        self.assertEqual(a, ["spam", "eggs", 100, 1234])
        a[2] = a[2] + 23
        self.assertEqual(a, ["spam", "eggs", 123, 1234])

        # Assignment to slices is also possible, and this can even change the size of
        # the list or clear it entirely:
        # Replace some items:
        a[0:2] = [1, 12]
        self.assertEqual(a, [1, 12, 123, 1234])
        # Remove some:
        a[0:2] = []
        self.assertEqual(a, [123, 1234])
        # Insert some:
        a[1:1] = ["bletch", "xyzzy"]
        self.assertEqual(a, [123, "bletch", "xyzzy", 1234])
        # Insert (a copy of) itself at the beginning
        a[:0] = a
        self.assertEqual(
            a, [123, "bletch", "xyzzy", 1234, 123, "bletch", "xyzzy", 1234]
        )
        # Clear the list: replace all items with an empty list
        a[:] = []
        self.assertEqual(a, [])

        # The built-in function len() also applies to lists:
        a = ["a", "b", "c", "d"]
        self.assertEqual(4, len(a))

        # It is possible to nest lists (create lists containing other lists), for
        # example:
        q = [2, 3]
        p = [1, q, 4]
        self.assertEqual(len(p), 3)
        self.assertEqual(p[1], [2, 3])
        self.assertEqual(p[1][0], 2)
        p[1].append("xtra")  # see tutorial_5 !
        self.assertEqual(p, [1, [2, 3, "xtra"], 4])
        self.assertEqual(q, [2, 3, "xtra"])


if __name__ == "__main__":
    unittest.main()
