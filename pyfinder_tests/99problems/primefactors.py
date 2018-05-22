import itertools
from symbolic.args import *
#JH: Fails because list is unhashable. Sol'n would be to deal with tuples
#TODO: convert to tuples recursively in loader.py
def prime_factors(value):
    """ trial divisions are all primes because of previous reductions of value
        print list(factors(1234567890987654321))
    """
    if value > 3:
        for this in itertools.chain(iter([2]), range(3,int(value ** 0.5)+1, 2)):
            if this*this > value:  break
            while not (value % this):
                if value == this: break
                value /=  this
                yield this
    yield value

@symbolic(n=315)
def primefactors(n):
    """return list [ [p_0,k_0], [p_1,k_1], ... ], where there are 'k_i'
    occurrences of 'p_i' in the prime factorization of n.

    >>> prime_factors_mult(315)
    [[3, 2], [5, 1], [7, 1]]
    """
    res = list(prime_factors(n))
    return sorted([int(fact), res.count(fact)] for fact in set(res))


def expected_result():
    return [[3, 2], [5, 1], [7, 1]]

#print(primefactors(315))
