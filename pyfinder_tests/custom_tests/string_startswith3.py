from symbolic.args import *


# This test has to be run with the --cvc flag
# This is one of 4 test cases. We compare using:
# "Hello World".startswith(a)
# Here we seed a symbolic string that fits in the
# second branch. Unlike the 1st test case, this
# fails for reasons not entirely understood.
# Although CVC tried "Hello World" in the 1st test case, it
# does not do so here.
# later update (jteoh): I suspect this is because the LHS
# is a literal string (as opposed to symbolic), and thus
# the concrete startswith function is called. No symbolic
# expression is retained, so there's no way to use the
# solvers.
# in contrast, a.startswith works because `a` is wrapped
# into a symbolic string.
# naive/first thought proposal is two-step (might be able
# to use just one though?), both involving preprocess:
# 1. If a function is commutative and the leftmost argument is
#       not symbolic, swap the order so that it is. eg:
#               "Hello World" == a
#               is swapped to
#               a == "Hello World"
#       This does not capture non-commutative operations though... so
# 2. preprocess the program and explicitly wrap any constant values with
#       symbolic versions. This requires a little more consideration still.
@symbolic(a="xyz")
def string_startswith3(a):
    if ("Hello World".startswith(a)):
        return "foo"
    else:
        return "bar"


def expected_result():
    return ["foo", "bar"]
