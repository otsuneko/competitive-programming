import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

H,W = map(int,input().split())
C = [list(input()) for _ in range(H)]

flg = [[0]*W for _ in range(H)]
flg_inv = [[0]*H for _ in range(W)]


for h in range(H):
    for w in range(1,W):
        if 