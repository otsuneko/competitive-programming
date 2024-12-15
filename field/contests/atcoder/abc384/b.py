import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,R = map(int,input().split())
ARC = [list(map(int,input().split())) for _ in range(N)]

for d,a in ARC:
    if d == 1 and 1600 <= R <= 2799:
        R += a
    elif d == 2 and 1200 <= R <= 2399:
        R += a
print(R)
