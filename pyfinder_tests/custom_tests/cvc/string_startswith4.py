from symbolic.args import *


# This test has to be run with the --cvc flag
# This is one of 4 test cases. We compare using:
# "Hello World".startswith(a)
# Here we seed a symbolic string that fits in the
# first branch. Unlike the 2st test case, an empty
# input "" would still fit in the first test case.
# later update (jteoh): see string_startswith3.py to
# help explain this behavior.
@symbolic(a="Hello")
def string_startswith4(a):
    if ("Hello World".startswith(a)):
        return "foo"
    else:
        return "bar"


def expected_result():
    return ["foo", "bar"]
