import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

K,G,M = map(int,input().split())

glass = 0
cup = 0
while K:
    K -= 1
    if glass == G:
        glass = 0
    elif cup == 0:
        cup = M
    else:
        move = min(cup, G - glass)
        glass += move
        cup -= move

print(glass,cup)