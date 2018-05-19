from symbolic.args import *

# This test has to be run with the --cvc flag
# This is one of 4 test cases. We compare using:
# "Hello World".startswith(a)
# Here we seed a symbolic string that fits in the
# second branch. Unlike the 1st test case, this
# fails for reasons not entirely understood.
# Although CVC tried "Hello World" in the 1st test case, it
# does not do so here.
@symbolic(a="xyz")
def string_startswith3(a):
	if ("Hello World".startswith(a)):
		return "foo"
	else:
		return "bar"


def expected_result():
	return [ "foo", "bar" ]

