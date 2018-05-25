from symbolic.args import *

# This fails because there is no general symbolic type for data objects.
# (it won't even run, with either solver)
# this additional test is testing if we can still get source code for DataObj through an import.
from pyfinder_tests.custom_tests.data_obj import DataObj


@symbolic(a=DataObj(100))
def data_obj2(a):
    if a.value == 0:
        return 0
    elif a.value == 100:
        return 1
    else:
        return 2


def expected_result():
    return [0, 1, 2]