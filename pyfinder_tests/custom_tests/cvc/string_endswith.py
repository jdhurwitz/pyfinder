from symbolic.args import *


# This test has to be run with the --cvc flag
# SymbolicStr does not support endswith (despite supporting startswith)
# Here we explicitly make sure that the LHS is the symbolic string, as
# PyExZ3 is unable to wrap string constants (non-arguments) into symbolic
# versions.
# TL;DR: endswith here is the native string endswith, rather than one
# implemented by PyExZ3 to support symbolic execution.
@symbolic(a="World")
def string_endswith(a):
    # if ("Hello World".endswith(a)):
    if (a.endswith("Hello World")):
        return "foo"
    else:
        return "bar"


def expected_result():
    return ["foo", "bar"]
