from symbolic.args import *


# This test has to be run with the --cvc flag
# By seeding with "",
# the ATP is able to infer that the other value should be "Hello World"
# Without this, PyExZ3 will fail because it cannot compare an int (a) 
# and a String
# Ideally, this should be solvable without passing a seed string (symbolic)
# This represents a small, easy fix that we can implement.
@symbolic(a="")
def string_cmp(a):
    if (a == "Hello World"):
        return "foo"
    else:
        return "bar"


def expected_result():
    return ["foo", "bar"]
