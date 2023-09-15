import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

M = int(input())
D = list(map(int,input().split()))

half = sum(D)//2

su = 0
for i in range(M):
    if su + D[i] > half:
        print(i+1, half-su+1)
        break
    su += D[i]