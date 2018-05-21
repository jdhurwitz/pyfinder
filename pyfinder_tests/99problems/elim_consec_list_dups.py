from itertools import groupby

#JH: this fails because of lack of symbolic list support
@symbolic(aList=[1,1,2,2,3,3])
def compress(alist):
    return [key for key, group in groupby(alist)]

def expected_result():
	return [1,2,3]