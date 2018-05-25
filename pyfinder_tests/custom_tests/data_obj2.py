from symbolic.args import *

# This fails because there is no general symbolic type for data objects.
# (it won't even run, with either solver)
# this additional test is testing if we can still get source code for DataObj through an import.
from pyfinder_tests.custom_tests.data_obj import DataObj


@symbolic(a=DataObj("foo"))
def data_obj(a):
    if a == "foo":
        return 0
    elif a == "bar":
        return 1
    else:
        return 2


def expected_result():
    return [0, 1, 2]