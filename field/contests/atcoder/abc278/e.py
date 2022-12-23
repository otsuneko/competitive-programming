H,W,N,h,w = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(H)]
from collections import defaultdict
dict = defaultdict(int)

for h in range(H):
    for w in range(W):
        dict[A[h][w]] += 1

for k in range(H-h+1):
    for l in range(W-w+1):
        for h in range(k,k+h+1):
            for 