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

from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


# Installing avro from PyPI
avro_install_requires = "avro==1.10.2"

# Example of avro installed locally
# avro_install_requires = (
#    "avro"
#    f"@file://localhost{os.path.expanduser('~')}/working/apache/avro/dist/py/"
#    "avro-1.12.0+snapshot-py2.py3-none-any.whl"
# )

setup(
    name="python-scripts",
    version="0.1",
    description="My Python scripts, examples and how-tos.",
    long_description=readme(),
    url="http://github.com/RyanSkraba/python-examples",
    author="Ryan Skraba",
    author_email="ryan@skraba.com",
    license="ASL",
    packages=["scanscan"],
    scripts=["bin/hello-world"],
    install_requires=[avro_install_requires, "docopt==0.6.2"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
    ],
    tests_require=["pytest==6.2.5"],
    zip_safe=False,
)
