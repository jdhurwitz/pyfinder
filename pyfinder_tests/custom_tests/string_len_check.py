from symbolic.args import *

# This test has to be run with the --cvc flag because it uses strings.
# Surprisingly, CVC is able to generate strings ("AA") that satisfy
# the length check. If you were to replace "dummy" with a 2-char string,
# CVC would also be able to generate an empty string input.
@symbolic(a="dummy")
def string_len_check(a):
	if (len(a) == 2):
		return "foo"
	else:
		return "bar"


def expected_result():
	return [ "foo", "bar" ]

