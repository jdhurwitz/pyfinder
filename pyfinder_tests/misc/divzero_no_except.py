# this one fails because we always start with zero for SymbolicIntegers
# we should have a few seed values to avoid this.

def divzero_no_except(in1, in2):

    if in1 // in2 >= 0:
        return 1
    elif in1 // in2 < 0:
        return 2
    return 0



def expected_result():
    return [1, 2]