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
from typing import Any, Tuple

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

CODE_EVAL = """\
output = eval("input[0] + input[1]")
"""

CODE_COMPILE_EVAL = """\
fn_ast = compile("lambda x: (x[0] + x[1])", "<string>", "eval")
fn = eval(fn_ast)
output = fn(input)
"""

CODE_EXEC = """\
return_values = {"num": input}
exec("sum = num[0] + num[1]", None, return_values)
output = return_values["sum"]
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

CODE_OSNAME_IMPORT = """\
os = __import__('os')
output = "Hello %s from %s" % (input, os.name)
"""

CODE_OSNAME_IMPORT_INDIRECT = """\
module_os = "os"
os = __import__(module_os)
output = "Hello %s from %s" % (input, os.name)
"""

CODE_OSNAME_BUILTINS = """\
output = "Hello %s from %s" % (input, __builtins__['__import__']("os").name)
"""

CODE_OSNAME_BUILTINS_IMPORT = """\
output = "Hello %s from %s" % (input, __builtins__["__import__"]("os").name)
"""

CODE_OSNAME_BUILTINS_MODULE = """\
import builtins
output = "Hello %s from %s" % (input, builtins.__dict__['__import__']("os").name)
"""

CODE_OSNAME_IMPORTLIB_MODULE = """\
import importlib
os = importlib.import_module("os")
output = "Hello %s from %s" % (input, os.name)
"""

LAMBDA_SUM = """\
input[0] + input[1]
"""

LAMBDA_OSNAME = """\
"Hello %s from %s" % (input, __import__('os').name)
"""

CODE_CLASS = """\
class MyClass(object): pass

output = MyClass.__class__.__name__
"""

CODE_BASES = """\
class MyClass(object): pass
class MySubClassA(MyClass): pass

output = [cls.__name__ for cls in MySubClassA.__bases__]
"""

CODE_SUBCLASSES = """\
class MyClass(object): pass
class MySubClassA(MyClass): pass
class MySubClassB(MyClass): pass
class MySubClassASubClass(MySubClassA): pass

output = [cls.__name__ for cls in MyClass.__subclasses__()]
"""


class AstScanner(ast.NodeVisitor):
    def __init__(self):
        self.log = logging.getLogger(__name__)
        # All of the __special__ methods and attributes used.
        self.double_underscore = set()
        # All of the modules imported by the code
        self.modules = set()

    def generic_visit(self, node: ast.AST) -> Any:
        self.log.debug("AST: %s", node)
        super().generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        if node.attr.startswith("__"):
            self.double_underscore.add(node.attr)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        if isinstance(node.func, ast.Name) and node.func.id.startswith("__"):
            self.double_underscore.add(node.func.id)
        if (
            isinstance(node.func, ast.Name)
            and node.func.id == "__import__"
            and len(node.args) > 0
        ):
            module = node.args[0]
            if isinstance(module, ast.Constant):
                self.modules.add(module.value)
            elif isinstance(module, ast.Str):
                self.modules.add(module.s)
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


def udfize_lambda_string(expression: str):
    """Given an expression that uses 'input' as a parameter, return a lambda as a string."""
    return "lambda input: ({})".format(expression)


def udfize_lambda(expression: str, glb_ctx: dict = None, lcl_ctx: dict = None):
    if lcl_ctx is None:
        lcl_ctx = {}
    if glb_ctx is None:
        glb_ctx = {}
    return eval(
        compile(udfize_lambda_string(expression), "<string>", "eval"), glb_ctx, lcl_ctx
    )


def udfize_def_string(code: str) -> str:
    """Given an unindented code block that uses 'input' as a parameter, and output as a
    return value, returns a function as a string."""
    return """\
def udf(input):
 {}
 return output
""".format(
        " ".join(line for line in code.splitlines(True))
    )


def udfize_def(
    code: str, glb_ctx: dict = None, lcl_ctx: dict = None
) -> Tuple[Any, AstScanner]:
    if lcl_ctx is None:
        lcl_ctx = {}
    if glb_ctx is None:
        glb_ctx = {}

    udf_ast = ast.parse(udfize_def_string(code), filename="<udf>")

    finder = AstScanner()
    finder.visit(udf_ast)

    # Executing this code here is simply defining a method.
    exec(compile(udf_ast, filename="<udf>", mode="exec"), glb_ctx, lcl_ctx)
    return lcl_ctx["udf"], finder


class AstModuleTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_exec_with_system_globals(self):
        # Compile the UDF using the system globals
        self.assertNotIn("udf", globals())
        udf_ast = compile(UDF_DEF_GLOBAL_SUM, "<string>", "exec")
        ret = exec(udf_ast)

        self.assertIn("udf", globals())
        self.assertIsNone(ret)
        # No matter what the IDE claims, it is actually defined now!
        self.assertEqual(udf(100, 23), 123)  # noqa: F821
        self.assertEqual(udf(100, 23000), 23100)  # noqa: F821
        # Clean it up.
        del globals()["udf"]

    def test_exec_with_user_globals(self):
        udf_ast = compile(UDF_DEF_GLOBAL_SUM, "<string>", "exec")
        glb_ctx = {}
        exec(udf_ast, glb_ctx)

        # UDF shouldn't be available in any space!
        self.assertNotIn("udf", globals())
        self.assertNotIn("udf", dir())
        self.assertIn("udf", glb_ctx)

        with self.assertRaises(NameError) as cm:
            udf(100, 23)  # noqa: F821
        self.assertIn(
            "local variable 'udf' referenced before assignment", cm.exception.args
        )

        udf = glb_ctx["udf"]
        self.assertEqual(udf(100, 23), 123)
        self.assertEqual(udf(100, 23000), 23100)

    def test_exec_with_user_locals(self):
        udf_ast = compile(UDF_DEF_SUM, "<string>", "exec")
        glb_ctx = {}
        lcl_ctx = {}
        exec(udf_ast, glb_ctx, lcl_ctx)

        # UDF shouldn't be available in any space!
        self.assertNotIn("udf", globals())
        self.assertNotIn("udf", dir())
        self.assertNotIn("udf", glb_ctx)
        self.assertIn("udf", lcl_ctx)
        udf = lcl_ctx["udf"]
        self.assertEqual(udf(100, 23), 123)
        self.assertEqual(udf(100, 23000), 23100)

    def test_exec_sum_udfsize_string(self):
        udfstr = udfize_def_string(CODE_SUM)
        udf_ast = compile(udfstr, "<string>", "exec")
        glb_ctx = {}
        lcl_ctx = {}
        exec(udf_ast, glb_ctx, lcl_ctx)

        # UDF shouldn't be available in any space!
        self.assertNotIn("udf", globals())
        self.assertNotIn("udf", dir())
        self.assertNotIn("udf", glb_ctx)
        self.assertIn("udf", lcl_ctx)
        udf = lcl_ctx["udf"]
        self.assertEqual(udf([100, 23]), 123)
        self.assertEqual(udf([100, 23000]), 23100)

    def test_exec_sum_udfize(self):
        udf, scan = udfize_def(CODE_SUM)
        self.assertEqual(udf([100, 23]), 123)
        self.assertEqual(udf([100, 23000]), 23100)
        udf, scan = udfize_def(CODE_EVAL)
        self.assertEqual(udf([100, 24]), 124)
        self.assertEqual(udf([100, 24000]), 24100)
        udf, scan = udfize_def(CODE_COMPILE_EVAL)
        self.assertEqual(udf([100, 25]), 125)
        self.assertEqual(udf([100, 25000]), 25100)
        udf, scan = udfize_def(CODE_EXEC)
        self.assertEqual(udf([100, 26]), 126)
        self.assertEqual(udf([100, 26000]), 26100)

    def test_exec_osname_udfize(self):
        udf, scan = udfize_def(CODE_OSNAME)
        self.assertEqual(udf("World1"), "Hello World1 from posix")
        udf, scan = udfize_def(CODE_OSNAME_AS)
        self.assertEqual(udf("World2"), "Hello World2 from posix")
        udf, scan = udfize_def(CODE_OSNAME_FROM)
        self.assertEqual(udf("World3"), "Hello World3 from posix")
        udf, scan = udfize_def(CODE_OSNAME_FROM_AS)
        self.assertEqual(udf("World4"), "Hello World4 from posix")
        udf, scan = udfize_def(CODE_OSNAME_IMPORT)
        self.assertEqual(udf("World5"), "Hello World5 from posix")
        udf, scan = udfize_def(CODE_OSNAME_IMPORT_INDIRECT)
        self.assertEqual(udf("World6"), "Hello World6 from posix")
        udf, scan = udfize_def(CODE_OSNAME_BUILTINS)
        self.assertEqual(udf("World7"), "Hello World7 from posix")
        udf, scan = udfize_def(CODE_OSNAME_BUILTINS_IMPORT)
        self.assertEqual(udf("World8"), "Hello World8 from posix")
        udf, scan = udfize_def(CODE_OSNAME_BUILTINS_MODULE)
        self.assertEqual(udf("World9"), "Hello World9 from posix")
        udf, scan = udfize_def(CODE_OSNAME_IMPORTLIB_MODULE)
        self.assertEqual(udf("World10"), "Hello World10 from posix")

    def test_exec_sum_udfize_with_no_builtins(self):
        udf, scan = udfize_def(CODE_SUM, glb_ctx=GLOBALS_NO_BUILTINS)
        self.assertEqual(udf([100, 23]), 123)
        self.assertEqual(udf([100, 23000]), 23100)

    def test_exec_osname_udfize_with_no_builtins(self):
        # This generates an error because the import can't be done if the built-ins aren't available
        udf, scan = udfize_def(CODE_OSNAME, glb_ctx=GLOBALS_NO_BUILTINS)
        if sys.version_info.minor <= 7:
            with self.assertRaises(ImportError):
                udf("World")
        else:
            with self.assertRaises(SystemError):
                udf("World")

    def test_exec_doubleunderscore_class(self):
        udf, scan = udfize_def(CODE_CLASS)
        self.assertEqual(udf(None), "type")

    def test_exec_doubleunderscore_bases(self):
        udf, scan = udfize_def(CODE_BASES)
        self.assertEqual(udf(None), ["MyClass"])

    def test_exec_doubleunderscore_subclasses(self):
        udf, scan = udfize_def(CODE_SUBCLASSES)
        self.assertEqual(udf(None), ["MySubClassA", "MySubClassB"])

    def test_exec_with_errors(self):
        # Everything is fine.
        udf, scan = udfize_def("""output = "Everything is {}!".format(input) """)
        self.assertEqual(udf("great!"), "Everything is great!!")

        # The parameter is input, not incoming.  The syntax is fine though.
        udf, scan = udfize_def("""output = "Everything is {}!".format(incoming) """)
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
            finder = AstScanner()
            finder.visit(ast.parse(code, "<string>", "exec"))
            self.assertEqual(finder.modules, {"os"})
            self.assertEqual(finder.double_underscore, set())
        for code in [CODE_OSNAME_FROM, CODE_OSNAME_FROM_AS]:
            finder = AstScanner()
            finder.visit(ast.parse(code, "<string>", "exec"))
            self.assertEqual(finder.modules, {"os"})
            self.assertEqual(finder.double_underscore, set())
        for code in [CODE_OSNAME_IMPORT]:
            finder = AstScanner()
            finder.visit(ast.parse(code, "<string>", "exec"))
            self.assertEqual(finder.modules, {"os"})
            self.assertEqual(finder.double_underscore, {"__import__"})
        for code in [CODE_OSNAME_IMPORT_INDIRECT]:
            finder = AstScanner()
            finder.visit(ast.parse(code, "<string>", "exec"))
            # It can't find the import name since it's a variable, not a constant.
            self.assertEqual(finder.modules, set())
            self.assertEqual(finder.double_underscore, {"__import__"})

    def test_scan_ast_lambda_osname(self):
        finder = AstScanner()
        finder.visit(ast.parse(LAMBDA_OSNAME, "<string>", "exec"))
        # It's imported via __imports__
        self.assertEqual(finder.modules, {"os"})
        self.assertEqual(finder.double_underscore, {"__import__"})


if __name__ == "__main__":
    unittest.main()
