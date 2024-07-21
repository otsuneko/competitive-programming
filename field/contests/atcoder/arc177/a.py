import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

A,B,C,D,E,F = map(int,input().split())
N = int(input())
X = list(map(int,input().split()))

for x in X:
    while x >= 500 and F > 0:
        x -= 500
        F -= 1
    while x >= 100 and E > 0:
        x -= 100
        E -= 1
    while x >= 50 and D > 0:
        x -= 50
        D -= 1
    while x >= 10 and C > 0:
        x -= 10
        C -= 1
    while x >= 5 and B > 0:
        x -= 5
        B -= 1
    while x >= 1 and A > 0:
        x -= 1
        A -= 1
    if x != 0:
        print("No")
        exit()
print("Yes")
