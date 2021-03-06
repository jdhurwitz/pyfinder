from symbolic.args import *


# Very far reach goal
class DataObj:
    """ Simple data object with one value and straightforward constructor"""

    def __init__(self, value):
        self.value = value


# This fails because there is no general symbolic type for data objects.
# (it won't even run, with either solver)
@symbolic(a=DataObj(100))
def data_obj(a):
    if a.value == 0:
        return 0
    elif a.value == 100:
        return 1
    else:
        return 2


def expected_result():
    return [0, 1, 2]
