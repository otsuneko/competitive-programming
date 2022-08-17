from itertools import groupby

N =int(input())
A = list(map(int,input().split()))

cur = A[0]

for i in range(1,N):
    if A[i] >= cur:
        cur = A[i]
    else:
        break

ans = [str(a) for a in A if a != cur]
print(" ".join(ans))