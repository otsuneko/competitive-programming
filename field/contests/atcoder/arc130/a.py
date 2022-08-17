def nCr(n, r):

    res = 1
    for i in range(r):
        res = (res*(n-i))//(i+1)

    return res

import itertools

N = int(input())
S = input()

ans = 0

group = itertools.groupby(S)

for k,v in group:
    ans += nCr(len(list(v)),2)

print(ans)
