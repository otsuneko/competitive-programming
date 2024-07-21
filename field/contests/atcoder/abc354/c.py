import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = []
C = []
for i in range(N):
    a,c = map(int, input().split())
    A.append(a)
    C.append((c,i))
C.sort()

ma = 0
ans = []
for c,i in C:
    if ma < A[i]:
        ans.append(i+1)
    ma = max(ma, A[i])
print(len(ans))
print(*sorted(ans))
