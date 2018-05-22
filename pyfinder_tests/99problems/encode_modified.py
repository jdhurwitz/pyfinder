def encode_modified(alist):
        def aux(lg):
            if len(lg)>1: return [len(lg), lg[0]]
            else: return lg[0]
        return [aux(list(group)) for key, group in groupby(alist)]
