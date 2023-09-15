import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = list(map(int,input().split()))

ans = []
tmp = 0
for i in range(len(A)):
    if i%7 == 0:
        ans.append(tmp)
        tmp = 0
    tmp += A[i]
ans.append(tmp)
print(*ans[1:])