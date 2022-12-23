def compare(f, u):
    if f + u < u + f:
        return -1
    elif f + u == u + f:
        return 0
    else:
        return 1

from functools import cmp_to_key

N,K = map(int,input().split())
S = [input() for _ in range(N)]

print(''.join(sorted(S, key = cmp_to_key(compare))[:K]))