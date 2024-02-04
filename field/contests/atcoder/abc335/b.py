import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())

ans = []
for x in range(22):
    for y in range(22):
        for z in range(22):
            if x+y+z <= N:
                ans.append((x,y,z))

ans.sort()
for a in ans:
    print(*a)