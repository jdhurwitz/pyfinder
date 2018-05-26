from symbolic.args import *

def gcd(a,b):
    """Return the gcd of two positive integers.

    >>> gcd(36,63)
    9
    >>> gcd(63,36)
    9
    """

    while b != 0:
        a, b = b, a%b
    return a

def coprime(a,b):
   """return True if 'a' and 'b' are coprime.

   >>> coprime(35,64)
   True
   """

   return gcd(a,b) == 1

@symbolic(m=10)
def totient(m):
    """calculate Euler's totient function using a primitive method.

    >>> phi(1)
    1
    >>> phi(10)
    4
    """

    if m == 1:
        return 1
    else:
        r = [n for n in range(1,m) if coprime(m,n)]
        return len(r)


"""
This test explores m=10 first, returning 4 as expected. The following exploration occurs:
m=1 1
m=0 0
m=3 2
m=6 2
m=8 4
m=4 2
m=22 10

However, program appears to hang at m=22.
TODO: investigate hang and add full set of expected results  
"""
def expected_result():
    return 4

