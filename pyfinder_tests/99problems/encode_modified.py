from symbolic.args import *
from itertools import groupby

#lack of symbolic list support
@symbolic(alist=[1,2,3,4,4,5])
def encode_modified(alist):
        def aux(lg):
            if len(lg)>1: return [len(lg), lg[0]]
            else: return lg[0]
        return [aux(list(group)) for key, group in groupby(alist)]

def expected_result():
    return {1: 1, 2: 1, 3: 1, '[2, 4]': 1, 5: 1}

#print(encode_modified([1,2,3,4,4,5]))