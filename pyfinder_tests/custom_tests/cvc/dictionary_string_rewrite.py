# Copyright: see copyright.txt
# jteoh: copying copyright message from test/dictionary.py

# This test must be run with --cvc
# Compare to dictionary_rewrite.py - this is just to demonstrate that strings work too.
from symbolic.args import *


@symbolic(in1="")  # until we also try seeded strings
def dictionary_string_rewrite(in1):
    d = {}
    d["foo"] = "bar"

    # general rewrite is similar to arrayindex(2).py.
    # Here we're looking if in1 matches a key, so
    # we create a list of all the keys that do match... but this could be very
    # inefficient depending on python implementation.
    if in1 in [j for j in d.keys() if in1 == j]:
        return 1
    else:
        return 2


def expected_result():
    return [1, 2]
