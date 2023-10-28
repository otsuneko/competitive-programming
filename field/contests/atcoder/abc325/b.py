import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
worlds = [list(map(int,input().split())) for _ in range(N)]

ans = 0
for i in range(25):
    su = 0
    for w,x in worlds:
        if 9<=(i+x)%24<=17:
            su += w
    ans = max(ans,su)
print(ans)