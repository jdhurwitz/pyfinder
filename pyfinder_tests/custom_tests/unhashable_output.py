from symbolic.args import *

# Unhashable types are generally those that are mutable. Common examples
# include lists, sets, and dictionaries. Note that tuples are considered
# immutable.
# TODO any others?
# This test idea came from discussion betweeen Jonathan and jteoh
# on 99problems/primefactors example.
# One fix: in the loader._toBag method, add a check if a value is hashable.
# if not, cast it to a string before hashing (roughly line 105)
# 			if not isinstance(i, collections.Hashable):
# 				i = str(i)
# (will need to import collections somewhere too)

list_val = [1]
set_val = {2}
dict_val = {3: 'foobar'}


def unhashable_output(a):
    if a == 1:
        return list_val
    elif a == 2:
        return set_val
    else:
        return dict_val


def expected_result():
    return [list_val, set_val, dict_val]
