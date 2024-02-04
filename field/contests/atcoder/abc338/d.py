import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,M = map(int,input().split())
X = list(map(int,input().split()))

ans = INF
start = X[0]
for stop_idx in range(N):
    cnt = 0
    for next in X[1:]:
        if start < stop_idx < next:
            cnt += N-(next-start)
        else:
            cnt += next-start
        start = next
    ans = min(ans,cnt)
print(ans)