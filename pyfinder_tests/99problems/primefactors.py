import itertools

#TODO: not sure why this fails?
@symbolic(n=315)
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
    return (value)

def prime_factors_mult(n):
    """return list [ [p_0,k_0], [p_1,k_1], ... ], where there are 'k_i'
    occurrences of 'p_i' in the prime factorization of n.

    >>> prime_factors_mult(315)
    [[3, 2], [5, 1], [7, 1]]
    """
    res = list(prime_factors(n))
    return sorted([fact, res.count(fact)] for fact in set(res))


def expected_result():
    return [[3, 2], [5, 1], [7, 1]]

