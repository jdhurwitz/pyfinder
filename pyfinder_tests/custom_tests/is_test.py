from symbolic.args import *


# This tests the "is" keyword. It fails because
# PyExZ3 wraps integer inputs into SymbolicInt,
# which then fail the identity check enforced by 'is'.
# This is an inherent limitation of the approach and
# cannot be remedied to the best of my knowledge.
@symbolic(a=0)
def is_test(a):
    if (a is 0):
        return "foo"
    else:
        return "bar"


def expected_result():
    return ["foo", "bar"]
