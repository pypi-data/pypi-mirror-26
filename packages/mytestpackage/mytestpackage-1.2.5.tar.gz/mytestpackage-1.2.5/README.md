# :package: Python Package

This is an example project for distributing a Python package to the [Python
Package Index (PyPI)](https://pypi.org) and [Anaconda
Cloud](https://anaconda.org). Suggestions for documenting the package and
running unit tests are also provided.

## Project Structure

Before developing your Python package, create an organized project folder to
contain the package and related files. The folder structure shown below
provides an example template for your project and assumes it will be hosted on
GitHub. Summaries of the folders and files in this project are given below.

```
python-package/
|- docs/
|- mytestpackage/
|- tests/
|- CONTRIBUTING.md
|- LICENSE
|- README.md
|- example.py
|- setup.py
```

`docs/` - Documentation for the package should be contained within the `docs/`
folder. [MkDocs](http://www.mkdocs.org) is a great project documentation tool
that uses Markdown files. [Sphinx](http://www.sphinx-doc.org/en/stable/) is
another common documentation tool that uses Restructured text files.

`mytestpackage/` - folder that contains the Python package. View the contents
of this folder for more details on how to construct your package. Notice the
use of the `__init__.py` files which inform Python to treat the directories as
containing packages.

`tests/` - folder containing unit test files. The
[pytest](https://docs.pytest.org/en/latest/) framework is the preferred testing
tool. The tests can be run from the terminal by entering the `pytest` command
from within the root directory for the project.

`CONTRIBUTING.md` - instructions for submitting code to the project's
repository on GitHub.

`LICENSE` - tells others how your code can be distributed. GitHub provides
several options for license files.

`README.md` - provides a description of the package and where to get more
details.

`example.py` - demonstrates importing the package and calling functions and
variables provided by the package.

`setup.py` - critical file that provides configuration settings for your
package. The contents of this file is based on the
[setup.py](https://github.com/kennethreitz/setup.py) guide by Kenneth Reitz.

## Distributing with PyPI

The [Python Package Index (PyPI)](https://pypi.org) is a repository of software
for the Python programming language. Package authors use PyPI to distribute
their software to the Python community. Use the steps below to upload your
package to PyPI. Also, make sure your package has a unique name that isn't
already taken by another developer.

### Step 1

Create an account on PyPI then install the twine tool to interact with the
package index from the command line.

```
pip install twine
```

### Step 2

Fill out the fields in `setup.py` with the appropriate information. See the
example setup file provided in this project for more details.

### Step 3

Upload your Python package to PyPI using the setup file. You will be asked for
the username and password you created earlier.

```
python setup.py upload
```

### Step 4

Wait for your package to get indexed in PyPI which can take up to 30 minutes.
You should eventually be able to `pip search` and `pip install` your package
once it is discoverable in the online system.

## Distributing with Anaconda Cloud

Here.

## References

The examples in this repository are based on the following references:
- [setup.py](https://github.com/kennethreitz/setup.py) by Kenneth Reitz
- [samplemod](https://github.com/kennethreitz/samplemod) by Kenneth Reitz
- [The HitchHiker's Guide to Python](http://docs.python-guide.org/en/latest/)
- [The Python Packaging Authority (PyPA)](https://www.pypa.io/en/latest/)

