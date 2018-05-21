from symbolic.args import *


# This test has to be run with the --cvc flag
# because PyExZ3 does not support None.
# This test fails because CVC is unable to infer
# "None" from the condition.
# The log actually shows path condition:
# (== a#0, None) (False)
# but CVC shows unsat.
# This is quite similar to test/cvc/none.py,
# but the else condition here is not explicit
# (compared to a != None) and the expected
# generated input correctly includes a case
# for the first branch (not included in none.py)
# We can actually remove this and rely on test/cvc/none.py
# if we fix it accordingly.
def fixed_none(c):
    if c == None:
        return 1
    else:  # if c != None:
        return 0


def expected_result_set():
    return {0, 1}
