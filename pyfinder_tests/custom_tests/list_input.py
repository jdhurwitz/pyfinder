from symbolic.args import *


# Quick demo to demonstrate that there is no symbolic list type.
@symbolic(a=[])
def list_input(a):
    if a[0]:
        return 0
    else:
        return 1


def expected_result():
    return [0, 1]
