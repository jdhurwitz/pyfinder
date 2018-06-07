#!/bin/sh
# This script serves more as a demonstration of how 
# to combine pyexz3 with coverage tools
# Assumes you have done the following:
#    pyenv install 3.2.3
#    pyenv install 3.6.5
# Example command
#    scripts/coverage.sh test/elseif.py
# It does the following steps
# 0: Setup, don't worry about these
# 1: Arguments: the test file (#1) and the ARGS (#2) - either '--cvc' or '--' (default)
# 2: PyExZ3 expects python 3.2.3 but coverage requires 
# whatever version is installed. Mine happens to be 3.6.5. 
# Before running PyExZ3, this script sets pyenv to use the right version.
# 3: Run pyexz3 as usual, making sure to use the --generate_test_suite flag.
# 4: Switch python versions back to 3.6.5
# 5: Run coverage analysis on the generated test suite
# 6: coverage-specific: generate html output for what has been collected.
# 7: open the html file for the input file (argument).
#		I also recommend checking out htmlcov/index.html for an overview.

# https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/..

# eg --cvc -t 5
ARGS="${@:2}"
FILE=$1

PYEXZ3_PYTHON_VERSION="3.2.3"
COVERAGE_PYTHON_VERSION="3.6.5"

# get current pyenv version
ORIG_PYENV_VERSION=$(pyenv version | cut -d ' ' -f1)
pyenv local $PYEXZ3_PYTHON_VERSION
python $DIR/pyexz3.py $FILE $ARGS --generate_test_suite
pyenv local $COVERAGE_PYTHON_VERSION
# hack: hope it's the most recently created file in test suite dir
TEST_FILE=$(ls -t $DIR/generated_test_suites | head -n 1)
coverage run --branch generated_test_suites/$TEST_FILE

coverage html
# for general viewing/high level view
# open htmlcov/index.html 
# However, we care mostly about the specific input file, so try to open that one.
# ugly sed usage: replace / or . with _ for the filename.
open htmlcov/$(sed -e 's/[\/.]/_/g' <<<"$FILE").html

# reset pyenv version
pyenv local $ORIG_PYENV_VERSION
