import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,S = map(int,input().split())
A = list(map(int,input().split()))

amari = S%sum(A)

A += A

from collections import deque
q=deque()
su = 0
for c in A:
    q.append(c)
    su += c

    while not su <= amari:
        rm=q.popleft() ## 条件を満たさないのでdequeの左端から要素を取り除く
        su -= rm

    if su == amari:
        print("Yes")
        exit()
print("No")
