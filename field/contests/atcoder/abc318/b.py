import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
rect = [list(map(int,input().split())) for _ in range(N)]

sheet = [["."]*101 for _ in range(101)]

for a,b,c,d in rect:
    for x in range(a,b):
        for y in range(c,d):
            sheet[x][y] = "#"

ans = 0
for x in range(101):
    for y in range(101):
        if sheet[x][y] == "#":
            ans += 1
print(ans)