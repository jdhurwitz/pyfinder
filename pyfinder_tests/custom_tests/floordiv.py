from symbolic.args import *


# This passes and is included as a partner to regular division.
# jteoh: not sure how // floor division is
# properly implemented though - it might be how z3 handles division for arithmetic ints (ie default behavior)
# either way, there's no 'simple' floor division test so this can act as one.
@symbolic(in1=6)
def floordiv(in1):
    if in1 // 5 == 1:
        return 0
    else:
        return 1


def expected_result():
    return [0, 1]
