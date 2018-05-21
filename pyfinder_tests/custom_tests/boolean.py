from symbolic.args import *


# This test HAS to use "is" here, because integer comparisons
# may still be true, eg '1 == True' is True.
# This test fails because PyExZ3 is unable to accurately
# use identity checks.
# An alternative would be to use effective booleans - that's
# covered in test/cvc/effectivebool.py
@symbolic(a=True) # even this still fails, because a is cast to a SymbolicInt
def boolean(a):
    if a is True:
        return 0
    elif a is False:
        return 1
    else:
        return 2


def expected_result():
    return [0, 1, 2]
