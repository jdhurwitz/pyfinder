from symbolic.args import *


# This test has to be run with the --cvc flag
# SymbolicStr does not support endswith (despite supporting startswith)
# Here we explicitly make sure that the LHS is the symbolic string, as
#
@symbolic(a="World")
def string_endswith(a):
    # if ("Hello World".endswith(a)):
    if (a.endswith("Hello World")):
        return "foo"
    else:
        return "bar"


def expected_result():
    return ["foo", "bar"]
