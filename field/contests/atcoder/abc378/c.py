import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = list(map(int,input().split()))

B = [-1]*N

from collections import defaultdict
dic = defaultdict(int)

for i in range(N):
    if A[i] in dic:
        B[i] = dic[A[i]]+1
        dic[A[i]] = i
    else:
        dic[A[i]] = i
print(*B)
