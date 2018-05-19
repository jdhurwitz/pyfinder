from symbolic.args import *


# This test has to be run with the --cvc flag
# This is one of 4 test cases. We compare using:
# a.startswith("Hello World")
# Here we seed a symbolic
# string that fits in the first branch. This succeeds
# for reasons not entirely known - it seems like CVC
# somehow knows to try the empty string as input?
@symbolic(a="Hello World lorem ipsum")
def string_startswith2(a):
	if (a.startswith("Hello World")):
	# if ("Hello World".startswith(a)):
		return "foo"
	else:
		return "bar"


def expected_result():
	return [ "foo", "bar" ]

