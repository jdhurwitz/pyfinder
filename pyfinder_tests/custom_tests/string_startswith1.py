from symbolic.args import *


# This test has to be run with the --cvc flag
# This is one of 4 test cases. We compare using:
# a.startswith("Hello World")
# Here we seed a symbolic
# string that fits in the second branch. This succeeds
# for reasons not entirely known - it seems like CVC
# somehow knows to try "Hello World" as input?
@symbolic(a="xyz")
def string_startswith1(a):
    if (a.startswith("Hello World")):
        return "foo"
    else:
        return "bar"


def expected_result():
    return ["foo", "bar"]
