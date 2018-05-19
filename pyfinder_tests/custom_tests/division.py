from symbolic.args import *

# This fails because PyExZ3 doesn't support the / operator,
# which would require a symbolic float (not implemented).
# As a result, the test is similar to failed/pow.py in that
# concrete execution is used in place of symbolic, and
# the theorem prover is never used.
@symbolic(in1=-6)
def division(in1):
    if in1 / 5 >= 0:
        return 1
    elif in1 / 5 < 0:
        return 2
    return 0
    
def expected_result():
    # 0 not actually reachable
    return [1,2]