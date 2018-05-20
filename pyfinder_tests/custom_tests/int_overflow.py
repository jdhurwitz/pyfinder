from symbolic.args import *


# This fails because both z3 and cvc are unable to
# solve for such a large value.
# In the case of z3, pyexz3's wrapper places an 
# integer bound that 10^128 exceeds (hence the error messages)
# Evaluation: I don't think we'll be able to support this 
# elegantly (efficiently) unless we introduce a new symbolic type 
# that specifically represents powers and some additional parsing
# to convert products appropriately (eg x*x --> x**2)

# @symbolic(x=10**64)
def int_overflow(x):
    if 10 ** 128 == x * x:
        return "POW"
    else:
        return "OTHER"


def expected_result():
    return ["OTHER", "POW"]
