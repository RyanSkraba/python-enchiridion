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
import ast
import logging
import sys
import unittest
from typing import Any

GLOBALS_NO_BUILTINS = {"__builtins__": None}

UDF_DEF_GLOBAL_SUM = """\
global udf
def udf(ina, inb):
  return ina + inb
"""

UDF_DEF_SUM = """\
def udf(ina, inb):
  return ina + inb
"""

UDF_LAMBDA_SUM = """\
lambda a, b: a + b
"""

CODE_SUM = """\
output = input[0] + input[1]
"""

CODE_OSNAME = """\
import os
output = "Hello %s from %s" % (input, os.name)
"""

CODE_OSNAME_AS = """\
import os as myos
output = "Hello %s from %s" % (input, myos.name)
"""

CODE_OSNAME_FROM = """\
from os import name
output = "Hello %s from %s" % (input, name)
"""

CODE_OSNAME_FROM_AS = """\
from os import name as myname
output = "Hello %s from %s" % (input, myname)
"""

LAMBDA_SUM = """\
input[0] + input[1]
"""

LAMBDA_OSNAME = """\
"Hello %s from %s" % (input, __import__('os').name)
"""


def udfize_lambda_string(code: str):
    """Return a string with the code as a function"""
    return "lambda input: ({})".format(code)


def udfize_lambda(input: str, glbCtx: dict = None, lclCtx: dict = None):
    if lclCtx is None:
        lclCtx = {}
    if glbCtx is None:
        glbCtx = {}
    return eval(
        compile(udfize_lambda_string(input), "<string>", "eval"), glbCtx, lclCtx
    )


def udfize_def_string(code: str) -> str:
    return """\
def udf(input):
 {}
 return output
""".format(
        " ".join(line for line in code.splitlines(True))
    )


def udfize_def(input: str, glbCtx: dict = None, lclCtx: dict = None):
    if lclCtx is None:
        lclCtx = {}
    if glbCtx is None:
        glbCtx = {}

    udf_ast = ast.parse(udfize_def_string(input), filename="<udf>")

    finder = UdfSecurityChecker()
    finder.visit(udf_ast)

    exec(compile(udf_ast, filename="<udf>", mode="exec"), glbCtx, lclCtx)
    return lclCtx["udf"]


class UdfSecurityChecker(ast.NodeVisitor):
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.uses_double_underscore = False
        # All of the modules imported by the code
        self.modules = set()

    def generic_visit(self, node: ast.AST) -> Any:
        self.log.debug("AST: %s", node)
        super().generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        if node.attr.startswith("__"):
            self.uses_double_underscore = True
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        if (
            isinstance(node.func, ast.Name)
            and node.func.id == "__import__"
            and len(node.args) > 0
        ):
            module = node.args[0]
            if isinstance(module, ast.Constant):
                self.modules.add(module.value)
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> Any:
        for alias in node.names:
            self.modules.add(alias.name)
            self.log.debug("IMPORTING: %s", alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        self.modules.add(node.module)
        for alias in node.names:
            self.log.debug("IMPORTING FROM: %s.%s", node.module, alias.name)
        self.generic_visit(node)


class AstModuleTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_exec_with_system_globals(self):
        # Compile the UDF using the system globals
        self.assertNotIn("udf", globals())
        udfast = compile(UDF_DEF_GLOBAL_SUM, "<string>", "exec")
        ret = exec(udfast)

        self.assertIn("udf", globals())
        self.assertIsNone(ret)
        # No matter what the IDE claims, it is actually defined now!
        self.assertEqual(udf(100, 23), 123)  # noqa: F821
        self.assertEqual(udf(100, 23000), 23100)  # noqa: F821
        # Clean it up.
        del globals()["udf"]

    def test_exec_with_user_globals(self):
        udfast = compile(UDF_DEF_GLOBAL_SUM, "<string>", "exec")
        glbCtx = {}
        exec(udfast, glbCtx)

        # UDF shouldn't be available in any space!
        self.assertNotIn("udf", globals())
        self.assertNotIn("udf", dir())
        self.assertIn("udf", glbCtx)

        with self.assertRaises(NameError) as cm:
            udf(100, 23)  # noqa: F821
        self.assertIn(
            "local variable 'udf' referenced before assignment", cm.exception.args
        )

        udf = glbCtx["udf"]
        self.assertEqual(udf(100, 23), 123)
        self.assertEqual(udf(100, 23000), 23100)

    def test_exec_with_user_locals(self):
        udfast = compile(UDF_DEF_SUM, "<string>", "exec")
        glbCtx = {}
        lclCtx = {}
        exec(udfast, glbCtx, lclCtx)

        # UDF shouldn't be available in any space!
        self.assertNotIn("udf", globals())
        self.assertNotIn("udf", dir())
        self.assertNotIn("udf", glbCtx)
        self.assertIn("udf", lclCtx)
        udf = lclCtx["udf"]
        self.assertEqual(udf(100, 23), 123)
        self.assertEqual(udf(100, 23000), 23100)

    def test_exec_sum_udfsize_string(self):
        udfstr = udfize_def_string(CODE_SUM)
        udfast = compile(udfstr, "<string>", "exec")
        glbCtx = {}
        lclCtx = {}
        exec(udfast, glbCtx, lclCtx)

        # UDF shouldn't be available in any space!
        self.assertNotIn("udf", globals())
        self.assertNotIn("udf", dir())
        self.assertNotIn("udf", glbCtx)
        self.assertIn("udf", lclCtx)
        udf = lclCtx["udf"]
        self.assertEqual(udf([100, 23]), 123)
        self.assertEqual(udf([100, 23000]), 23100)

    def test_exec_sum_udfize(self):
        udf = udfize_def(CODE_SUM)
        self.assertEqual(udf([100, 23]), 123)
        self.assertEqual(udf([100, 23000]), 23100)

    def test_exec_osname_udfize(self):
        udf = udfize_def(CODE_OSNAME)
        self.assertEqual(udf("World1"), "Hello World1 from posix")
        udf = udfize_def(CODE_OSNAME_AS)
        self.assertEqual(udf("World2"), "Hello World2 from posix")
        udf = udfize_def(CODE_OSNAME_FROM)
        self.assertEqual(udf("World3"), "Hello World3 from posix")
        udf = udfize_def(CODE_OSNAME_FROM_AS)
        self.assertEqual(udf("World4"), "Hello World4 from posix")

    def test_exec_sum_udfize_with_no_builtins(self):
        udf = udfize_def(CODE_SUM, glbCtx=GLOBALS_NO_BUILTINS)
        self.assertEqual(udf([100, 23]), 123)
        self.assertEqual(udf([100, 23000]), 23100)

    def test_exec_osname_udfize_with_no_builtins(self):
        # This generates an error because the import can't be done if the built-ins aren't available
        udf = udfize_def(CODE_OSNAME, glbCtx=GLOBALS_NO_BUILTINS)
        if sys.version_info.minor <= 7:
            with self.assertRaises(ImportError):
                udf("World")
        else:
            with self.assertRaises(SystemError):
                udf("World")

    def test_exec_with_errors(self):
        # Everything is fine.
        udf = udfize_def("""output = "Everything is {}!".format(input) """)
        self.assertEqual(udf("great!"), "Everything is great!!")

        # The parameter is input, not incoming.  The syntax is fine though.
        udf = udfize_def("""output = "Everything is {}!".format(incoming) """)
        with self.assertRaises(NameError) as cm:
            udf("broken")
        self.assertEqual(cm.exception.args, ("name 'incoming' is not defined",))

        # The parameter is input, not in.  The syntax is NOT fine -- in is a keyword.
        with self.assertRaises(SyntaxError) as cm:
            udfize_def("""output = "Everything is " + in""")
        self.assertEqual(cm.exception.msg, "invalid syntax")
        # There are two extra lines and one extra column added to the syntax error.
        # Otherwise, row 1 and column 29 is effectively where the error occurred.
        self.assertEqual(cm.exception.lineno - 2, 0)

        if sys.version_info.minor <= 7:
            self.assertEqual(cm.exception.offset - 1, 30)
        else:
            self.assertEqual(cm.exception.offset - 1, 29)

        # f strings are a feature after 3.5 and have different error offsets.
        if sys.version_info.minor <= 5:
            return

        # The parameter is input, not in.  The syntax is NOT fine -- in is a keyword.
        with self.assertRaises(SyntaxError) as cm:
            udfize_def("""output = f"Everything is {in}!" """)

        # But the line and offset are not in the original string, but in the interpolation.
        if sys.version_info.minor <= 7:
            self.assertEqual(cm.exception.msg, "invalid syntax")
            self.assertEqual(cm.exception.lineno, 1)
            self.assertEqual(cm.exception.offset, 3)
        elif sys.version_info.minor <= 8:
            self.assertEqual(cm.exception.msg, "invalid syntax")
            self.assertEqual(cm.exception.lineno, 1)
            self.assertEqual(cm.exception.offset, 2)
        else:
            self.assertEqual(cm.exception.msg, "f-string: invalid syntax")
            self.assertEqual(cm.exception.lineno, 2)
            self.assertEqual(cm.exception.offset, 2)

        print(cm.exception.__traceback__)

    def test_eval_lambda_sum_udfize(self):
        udf = udfize_lambda(LAMBDA_SUM)
        self.assertEqual(udf([100, 23]), 123)
        self.assertEqual(udf([100, 23000]), 23100)

    def test_eval_lambda_osname_udfize(self):
        udf = udfize_lambda(LAMBDA_OSNAME)
        self.assertEqual(udf("World"), "Hello World from posix")

    def test_scan_ast_code_osname(self):
        for code in [CODE_OSNAME, CODE_OSNAME_AS]:
            finder = UdfSecurityChecker()
            finder.visit(ast.parse(code, "<string>", "exec"))
            self.assertEqual(finder.modules, {"os"})
            self.assertFalse(finder.uses_double_underscore)
        for code in [CODE_OSNAME_FROM, CODE_OSNAME_FROM_AS]:
            finder = UdfSecurityChecker()
            finder.visit(ast.parse(code, "<string>", "exec"))
            self.assertEqual(finder.modules, {"os"})
            self.assertFalse(finder.uses_double_underscore)

    def test_scan_ast_lambda_osname(self):
        finder = UdfSecurityChecker()
        finder.visit(ast.parse(LAMBDA_OSNAME, "<string>", "exec"))
        # It's imported via __imports__
        self.assertEqual(finder.modules, {"os"})
        self.assertFalse(finder.uses_double_underscore)


if __name__ == "__main__":
    unittest.main()
