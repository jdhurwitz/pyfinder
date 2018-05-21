from symbolic.args import *


# This test has to be run with the --cvc flag
# By seeding with "",
# the ATP is able to infer that the other value should be "Hello World"
# Without this, PyExZ3 will fail because it cannot compare an int (a)
# and a String
# Ideally, this should be solvable without passing a seed string (symbolic)
# This represents a small, easy fix that we can implement.
# This is based on string_cmp.py, but swaps the arguments to demonstrate that
# this equality check is currently supported.
# jteoh: I'm not 100% sure, but I think this is because the python string impl for
# __eq__ will check and realize that `a` is not a string (instead it's symbolic), and
# throw a NotImplemented exception. Python sees this and assumes the operation is
# commutative so it tries a.__eq__(...), which works as expected. 
@symbolic(a="")
def string_cmp_commutative(a):
    if ("Hello World" == a):
        return "foo"
    else:
        return "bar"


def expected_result():
    return ["foo", "bar"]
