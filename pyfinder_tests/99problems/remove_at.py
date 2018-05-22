def remove_at(L, N):
        return L[N-1], L[:N-1] + L[N:]
