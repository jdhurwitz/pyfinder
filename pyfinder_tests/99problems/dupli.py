#Duplicate the elements of a list a given number of times
#L = list
#N = number of times
from symbolic.args import *


#No symbolic list type
@symbolic(L=[1,2,3], N=2)
def dupli(L, N):
      return [x for x in L for i in range(N)]

def expected_result():
      return {1: 2, 2: 2, 3: 2}
