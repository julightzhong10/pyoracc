pyoracc
=======

[![Build Status](https://travis-ci.org/oracc/pyoracc.svg?branch=master)](https://travis-ci.org/oracc/pyoracc) 
[![Maintainability](https://api.codeclimate.com/v1/badges/7244ac087b45146c5e3e/maintainability)](https://codeclimate.com/github/cdli-gh/pyoracc/maintainability)
[![codecov](https://codecov.io/gh/oracc/pyoracc/branch/master/graph/badge.svg)](https://codecov.io/gh/oracc/pyoracc)
[![DOI](https://zenodo.org/badge/19694984.svg)](https://zenodo.org/badge/latestdoi/19694984)

Python tools for working with ORACC/C-ATF files

Depends on PLY, Mako, Multiprocessing and Pytest

# Installation

If you don't use `pip`, you're missing out.
Here are [installation instructions](https://pip.pypa.io/en/stable/installing/).

Simply run:

```bash
    $ cd pyoracc
    $ git pull origin master
    $ pip install .
```

Or you can just do

    $ pip install git+git://github.com/cdli-gh/pyoracc.git 

Or you can also do

    $ pip install git+https://github.com/cdli-gh/pyoracc.git 


# Upgrading

If you already have installed it and want to upgrade the tool:

```bash
    $ cd pyoracc
    $ git pull origin master
    $ pip install . --upgrade
```

Or you can just do

    $ pip install git+git://github.com/cdli-gh/pyoracc.git --upgrade

Or you can also do

    $ pip install git+https://github.com/cdli-gh/pyoracc.git --upgrade


# Usage

To use it:

    $ pyoracc --help

*Only files with the .atf extension can be processed.  *
 
To run it on file:

    $ pyoracc -i ./pyoracc/test/data/cdli_atf_20180104.atf -f cdli

For a fresh copy of CDLI ATF, download the data bundle here : https://github.com/cdli-gh/data/blob/master/cdliatf_unblocked.atf

To run it on oracc file:

    $ pyoracc -i ./pyoracc/test/data/cdli_atf_20180104.atf -f oracc

To run it on folder:

    $ pyoracc -i ./pyoracc/test/data -f cdli
    
To disable segmentation (will be slow) and to run on whole, use switch -w/--whole:

    $ pyoracc -i ./pyoracc/test/data -f cdli -w
    
To see the console messages of the tool, use --verbose switch

    $ pyoracc -i ./pyoracc/test/data -f cdli --verbose

To output a summary, run parser without -w/--whole and use -s/--summary

    $ pyoracc -i ./pyoracc/test/data/cdli_atf_20180104.atf -f cdli -s [summary path]
    
Note that using the verbose option will also create a parselog.txt file, 
containing the log output along with displaying it on command line. 
The verbose output contains the lexical symbols, the parse grammer table
and the LR parsing table states.

Note that, if you parse a file contains mutiple ATF records under whole 
mode, the parser will stop whenever it meets a error and raise the info. 
If you want to see a summary of the whole file, you need to run without
-w/--whole. You may also use the -s/--summary to specify the output path
the summary when you run without -w/--whole.

Also note that, first time usage with any atf format will always display 
the parse tables irrespective of verbose switch.

If you don't give arguments, it will prompt for the path and atf file type.  

# Help

```bash
$ pyoracc --help
Usage: pyoracc [OPTIONS]

  My Tool does one work, and one work well.

Options:
  -i, --input_path PATH      Input the file/folder name.  [required]
  -f, --atf_type [cdli|atf]  Input the atf file type.  [required]
  -v, --verbose              Enables verbose mode
  -s, --summary              Input the summary path, only useful when run without -w/--whole
  --version                  Show the version and exit.
  --help                     Show this message and exit.

```

## Internal Dev Usage

### Development Guideline

* ORACC atf based changes will go in pyoracc/atf/oracc
* CDLI atf based changes will go in pyoracc/atf/cdli
* Common atf based changes will go in pyoracc/atf/common

### To run on directory

    $ python  -m pyoracc.model.corpus ./pyoracc/test/data  cdli

### To run on individual file

    $ python -m pyoracc.atf.common.atffile ./pyoracc/test/data/cdli_atf_20180104.atf cdli True

## Running Tests

Before running pytest and coverage, install [py.test](https://docs.pytest.org/en/latest/getting-started.html) and [pytest-cov](https://pypi.org/project/pytest-cov/).

    $ py.test --cov=pyoracc --cov-report xml --cov-report html --cov-report annotate --runslow

Before running pycodestyle, install [pycodestyle](https://pypi.org/project/pycodestyle/).

    $ pycodestyle

## API Consumption

```python
from pyoracc.atf.common.atffile import file_process
file_process(pathname, atftype, verbose)
```
