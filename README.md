The Python Enchiridion
==============================================================================

![Python Server CI](https://github.com/RyanSkraba/python-enchiridion/workflows/Python%20Server%20CI/badge.svg)

_[**Enchiridion**](https://en.wikipedia.org/wiki/Enchiridion): **A small manual or handbook.**_  It's a bit like a tech [cook book](https://www.oreilly.com/search/?query=cookbook), but a bigger, fancier, SEO-optimizabler word.

Links to python resources, examples, setup and temporary scripts.

Building and running
------------------------------------------------------------------------------

```bash
# Setting up and using virtualenv.
python -m venv env/
source env/bin/activate
pip install --upgrade pip

./setup.py test

# Create a distribution
pip install wheel
./setup.py sdist bdist_wheel

# Install from repo
./setup.py install

# Or install from wheel
pip install dist/python_scripts-*.whl

# After installing, you can run the script.

# Print usage instructions
hello-world --help

# Run a server.
hello-world                 # prints Hello, World!
hello-world --name=comrade  # prints Hello, comrade!
```

Testing and automation
------------------------------------------------------------------------------

### [Black](https://black.readthedocs.io/en/stable/): The uncompromising code formatter

```bash
pip install black
black bin/* scanscan/ tests/ setup.py 
```

### [Flake8](https://flake8.pycqa.org/en/latest/): Your Tool For Style Guide Enforcement

```bash
pip install flake8
flake8 bin/* scanscan/ tests/ setup.py
```

### [Nose](https://nose.readthedocs.io/en/latest/) is nicer testing for python

Nose appears to be unmaintained since 2016.

```bash
pip install nose
nosetests -v
```

### [pytest](https://pytest.org) helps you write better programs

```bash
pip install pytest
pytest -v
```

### [Tox](https://tox.readthedocs.io/en/latest/): standardize testing in Python

See [tox.ini](./tox.ini).

```bash
pip install tox
tox --skip-missing-interpreters
```

IntelliJ setup
------------------------------------------------------------------------------

* IntelliJ
  - [Using the Python plugin](https://www.jetbrains.com/help/idea/plugin-overview.html#63317)
  - Set up a Python SDK virtualenv in `$PROJECT/env`

Running in docker
------------------------------------------------------------------------------

```bash
docker run -it --volume $PWD:/opt/workdir --workdir /opt/workdir python:3.6 bash
```

Syntax and best practices
------------------------------------------------------------------------------

* Object-oriented programming
  - [Language Reference - Data Model](https://docs.python.org/3/reference/datamodel.html)
  - [Python in a Nutshell - Object oriented](https://www.oreilly.com/library/view/python-in-a/9781491913833/ch04.html)
  - [Understanding Object Instantiation and Metaclasses in Python](https://www.honeybadger.io/blog/python-instantiation-metaclass/)

* PEP
  - [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
  - [PEP 257 -- Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
  - [PEP 440 -- Version Identification and Dependency Specification](https://www.python.org/dev/peps/pep-0440/)

Standard modules
------------------------------------------------------------------------------

* The **`ast`** module ([doc][ast-doc], [tests][ast-tests]) - Abstract Syntax Trees
  - Scary example code:
    - [**_Scary1_**](https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html): has 
      some good discussion on how to sanitize
    - [**_Scary2_**](https://nedbatchelder.com/blog/201302/finding_python_3_builtins.html)
    - [**_Scary3_**](https://stackoverflow.com/questions/35804961/python-eval-is-it-still-dangerous-if-i-disable-builtins-and-attribute-access)
  - [Tutorial - Dynamic Python](https://realpython.com/python-eval-function/)
  - [Better docs](https://greentreesnakes.readthedocs.io/en/latest/)

* The **`http.server`** module ([doc][http-server-doc]) - HTTP servers

* The **`logging`** module ([doc][logging-doc], [tests][logging-tests]) - Logging facility for Python

* The **`re`** module ([doc][re-doc], [tests][re-tests]) - Regular expression operations

* The **`socket`** module ([doc][socket-doc], [tests][socket-tests]) - low-level networking interface
  - [Tutorial - Python sockets](https://realpython.com/python-sockets/)
  - [Unix domain sockets](https://pymotw.com/2/socket/uds.html)

* The **`socketserver`** module ([doc][socketserver-doc], [tests][ast-tests]) - A framework for network servers

* The **`unittest`** module ([doc][unittest-doc]) - Unit testing framework

[ast-doc]: https://docs.python.org/3/library/ast.html
[ast-tests]: ./tests/std_modules/test_module_ast.py
[http-server-doc]: https://docs.python.org/3/library/http.server.html
[logging-doc]: https://docs.python.org/3/library/logging.html
[logging-tests]: ./tests/std_modules/test_module_logging.py
[re-doc]: https://docs.python.org/3/library/re.html
[re-tests]: ./tests/std_modules/test_module_re.py
[socket-doc]: https://docs.python.org/3/library/socket.html
[socket-tests]: ./tests/std_modules/test_module_socket.py
[socketserver-doc]: https://docs.python.org/3/library/socketserver.html
[unittest-doc]: https://docs.python.org/3/library/unittest.html

Project packaging and setup
------------------------------------------------------------------------------

### How do you set up a project again?  What are all of those files for?

- [How To Package Your Python Code](https://python-packaging.readthedocs.io/en/latest/)
- [Hitchhiker's Guide - Structuring Your Project](https://docs.python-guide.org/writing/structure/)
- [Python packaging - Past, Present, Future](https://www.bernat.tech/pep-517-518/) (Feb 2019)
- Example code:
  - https://github.com/pypa/sampleproject
  - https://github.com/navdeep-G/samplemod
- [How to make an awesome Python package in 2021](https://antonz.org/python-packaging/)
- [How to create a Python package in 2022](https://mathspp.com/blog/how-to-create-a-python-package-in-2022)

### Files:

* [**`.gitignore`**][git-ignore-example]: Lots of examples of temporary and build files generated
  during the software lifecycle.
* [**`LICENSE`** (ASL-2)](https://www.apache.org/licenses/LICENSE-2.0): How you want your software 
  used and distributed. _See also setup.py_
* [**`MANIFEST.in`**][manifest-in-spec]: Files included in the source distribution
* **`README.md`**: This file, used in github but also in the distributed package.
* [**`setup.py`**][setup-py-spec] : Build python projects.
* [**`tox.ini`**][tox-ini-spec] : Used for coordinating builds and tests with tox.

[git-ignore-example]: https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore
[manifest-in-spec]: https://packaging.python.org/guides/using-manifest-in/
[setup-py-spec]: https://setuptools.readthedocs.io/en/latest/
[tox-ini-spec]: https://tox.readthedocs.io/en/latest/example/basic.html#a-simple-tox-ini-default-environments

### PyPI (the Python package index)

* [Package index mirrors and caches](https://packaging.python.org/guides/index-mirrors-and-caches/)

You can create a PyPI mirror like this:

```bash
# In one virtual env, download a package and put it in the mirror.
pip install piprepo
pip download --destination-directory /tmp/cache avro-python3==1.9.2 # Fails
pip download --destination-directory /tmp/cache avro-python3==1.9.2.1 
pip download --destination-directory /tmp/cache avro-python3==1.10.0 
pip download --destination-directory /tmp/cache avro-python3==1.10.1 
pip download --destination-directory /tmp/cache avro-python3==1.10.2 
pip download --destination-directory /tmp/cache avro-python3
pip download --destination-directory /tmp/cache wheel
pip download --destination-directory /tmp/cache pycodestyle
piprepo build /tmp/cache/
# The directory is now a cache of all the Avro packages

# In any other virtualenv, use the mirror.
pip install -i file:///tmp/cache/simple --force-reinstall avro-python3

# Or use a docker to isolate the installation.
docker run -it -v /tmp/cache/:/tmp/cache --network none python:3 \
    pip install -i file:///tmp/cache/simple --force-reinstall avro-python3
```
