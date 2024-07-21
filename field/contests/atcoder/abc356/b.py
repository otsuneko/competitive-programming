import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,M = map(int,input().split())
A = list(map(int,input().split()))
X = [list(map(int,input().split())) for _ in range(N)]

eiyou = [0]*M
for i in range(N):
    for j in range(M):
        eiyou[j] += X[i][j]

for i in range(M):
    if eiyou[i] < A[i]:
        print('No')
        exit()
print('Yes')
