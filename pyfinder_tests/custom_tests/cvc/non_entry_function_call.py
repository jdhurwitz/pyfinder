from symbolic.args import *


# This test has to be run with the --cvc flag
# This is based off of string_startswith3.py, and should fail if AST rewrite is disabled.
# despite name, this particular method is the primary entry point
@symbolic(a="xyz")
def non_entry_function_call(a):
    non_entry_point(a)

# this is an additional function call not found in the source code for the entry point.
def non_entry_point(a):
    if ("Hello World".startswith(a)):
        return "foo"
    else:
        return "bar"


def expected_result():
    return ["foo", "bar"]
