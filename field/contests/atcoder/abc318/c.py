import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,D,P = map(int,input().split())
F = list(map(int,input().split())) + [0]*(D-N%D)
F.sort(reverse=True)

cnt = 0
su = 0
for i in range(N+(D-N%D)):
    su += F[i]
    cnt += 1
    if cnt == D:
        if su > P:
            F[i] = F[i] - su + P
        su = 0
        cnt = 0
print(sum(F))