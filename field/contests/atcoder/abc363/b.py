import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,T,P = map(int,input().split())
L = list(map(int,input().split()))

for t in range(101):
    cnt = 0
    for i in range(N):
        if L[i] >= T:
            cnt += 1
    if cnt >= P:
        print(t)
        exit()
    for i in range(N):
        L[i] += 1
