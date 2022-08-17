from collections import Counter
N = int(input())
A = list(map(int,input().split()))

for i in range(N):
    A[i] = A[i]%200

d = Counter(A)
ans = 0
for key in d:
    ans += d[key]*(d[key]-1)//2

print(ans)