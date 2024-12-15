import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

H,W,X = map(int,input().split())
P,Q = map(int,input().split())
P,Q = P-1,Q-1
S = [list(map(int,input().split())) for _ in range(H)]

from heapq import heapify, heappush, heappop, heappushpop, heapreplace, nlargest, nsmallest  # heapqライブラリのimport

hq = []

MOVE = ([1, 0], [-1, 0], [0, 1], [0, -1]) #縦横移動
seen = set([(P,Q)])
for dy,dx in MOVE:
    ny,nx = P+dy,Q+dx
    if 0<=ny<H and 0<=nx<W:
        heappush(hq, (S[ny][nx],(ny,nx)))
        seen.add((ny,nx))

strength = S[P][Q]
while hq:
    slime,(y,x) = heappop(hq)
    if slime * X < strength:
        strength += slime
        for dy,dx in MOVE:
            ny,nx = y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and (ny,nx) not in seen:
                heappush(hq, (S[ny][nx], (ny,nx)))
                seen.add((ny,nx))

print(strength)
