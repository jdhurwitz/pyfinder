# Copyright: see copyright.txt
# jteoh: copying copyright message from test/dictionary.py

# Compare to dictionary_index.py
from symbolic.args import *


# @symbolic(in1=3) # including this allows for passing.
def dictionary_rewrite(in1):
    d = {}
    d[3] = 10

    # general rewrite is similar to arrayindex(2).py.
    # Here we're looking if in1 matches a key, so
    # we create a list of all the keys that do match... but this could be very
    # inefficient depending on python implementation.
    # jteoh later added: if I'm understanding write, python should use the iter
    # functionality if applicable, in which case this is reasonably acceptable.
    if in1 in [j for j in d.keys() if in1 == j]:
        return 1
    else:
        return 2


def expected_result():
    return [1, 2]
