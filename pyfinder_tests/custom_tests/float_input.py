from symbolic.args import *


# Quick demo to demonstrate that there is no symbolic float type.
@symbolic(a=1.5)
def float_test(a):
    if a > 1.1:
        return 0
    else:
        return 1


def expected_result():
    return [0, 1]
