from symbolic.args import *


# Quick demo to demonstrate that there is no symbolic float type.
def float_parse(a):
    if a > 1/5: # ie 0.2
        return 0
    else:
        return 1


def expected_result():
    return [0, 1]
