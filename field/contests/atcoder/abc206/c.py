def nCr(n, r):

    res = 1
    for i in range(r):
        res = (res*(n-i))//(i+1)

    return res

from collections import Counter
N = int(input())
A = list(map(int,input().split()))

d = Counter(A)

ans = nCr(N,2)
for k in d:
    ans -= nCr(d[k],2)
print(ans)