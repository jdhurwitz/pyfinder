from symbolic.args import *


# This test has to be run with the --cvc flag
# This is based off of string_startswith3.py, but is not a use case
# we can target with PyExZ3. While we do have support for basic function
# rewriting, this is currently limited only to the entry function
# (the below method) and not any additional method calls.
# While this example may seem easy enough to handle, things can get complex fast
# for example, what if the nested call is a runtime-generated function
# or a built-in function (for which there is python ast)?
@symbolic(a="xyz")
def non_entry_function_call(a):
    nested_call(a)

# this is an additional function call not found in the source code for the entry point.
def nested_call(a):
    if ("Hello World".startswith(a)):
        return "foo"
    else:
        return "bar"


def expected_result():
    return ["foo", "bar"]
