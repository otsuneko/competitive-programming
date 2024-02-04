import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from collections import defaultdict
dic = defaultdict(int)

N = int(input())
A = []
for _ in range(N):
    n = int(input())
    A.append(n)
    dic[n] += 1

ans = 0
for i in range(N):
    for k in range(N):
        if A[k]%A[i] == 0:
            ans += dic[A[k]//A[i]]
print(ans)