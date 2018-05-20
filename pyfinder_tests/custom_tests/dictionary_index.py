# Copyright: see copyright.txt
# jteoh: copying copyright message from test/dictionary.py

# Using concrete dictionary rather than the lib.se one
# which was specifically imported for test/dictionary.py
# and implements a has_key method.
# the 'in' method in python will call __contains__
# which is on the dictionary. Without somehow capturing
# information about the dictionary or wrapping it into
# a specialized class, we can't override __contains__ to
# capture the fact that a symbolic value is passed in.
# related: __r*__ methods (eg __radd__) likely wouldn't
# work here, as I believe dict does not throw a
# NotImplemented exception for any inputs.

from symbolic.args import *


# @symbolic(in1=3) # including this allows for passing.
def dictionary_index(in1):
    d = {}
    d[3] = 10

    if in1 in d:
        return 1
    else:
        return 2


def expected_result():
    return [1, 2]
