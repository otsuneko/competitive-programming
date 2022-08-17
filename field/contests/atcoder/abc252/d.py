def nCr(n, r):

    res = 1
    for i in range(r):
        res = (res*(n-i))//(i+1)

    return res

N = int(input())
A = list(map(int,input().split()))
A.sort()

# print(A)
from collections import Counter
count = Counter(A)

ans = nCr(N,3)
# print(count)
for key in count:
    if count[key] >= 3:
        # 3つ同じパターン
        ans -= nCr(count[key],3)
    if count[key] >= 2:
        # 2つ同じパターン
        ans -= nCr(count[key],2) * (N-count[key])

print(ans)