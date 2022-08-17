N,M = map(int,input().split())

parts = []
for _ in range(M):
    tmp = list(map(str,input().split()))
    S,C = list(tmp[0]), int(tmp[1])
    parts.append([S,C])

dp = [[10**18]*(2**N+1) for _ in range(N+1)]

for i in range(N):
    for j in range(2**N+1):
        