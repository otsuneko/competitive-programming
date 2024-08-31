import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

ans = 0
A,B = map(int,input().split())
for i in range(-1000,1000):
    li = sorted([A,B,i])
    if li[2]-li[1] == li[1]-li[0]:
        ans += 1
print(ans)
