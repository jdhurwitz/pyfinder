D =  dict({ (101,2), (1,3), (4,9) })

# Contrast with test/dict.py, this is
# a more general rewrite for the in comparator
# based on the python docs
# https://docs.python.org/3/reference/expressions.html#in
def collection_rewrite_by_docs(x):
    #
    if any(x is e or x == e for e in D):
       return D[x]
    else:
       return "NONE"

def expected_result():
    return [2,3,9,"NONE"]
