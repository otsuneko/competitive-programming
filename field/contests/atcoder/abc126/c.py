import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,K = map(int,input().split())

ans = 0

for dice in range(1,N+1):
    prob = 1/N
    score = dice
    while score < K:
        prob /= 2
        score *= 2
    ans += prob
print(ans)