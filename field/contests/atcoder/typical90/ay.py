from bisect import bisect
import itertools
from collections import defaultdict

N,K,P =map(int,input().split())
A = list(map(int,input().split()))

former = A[:N//2]
latter = A[N//2:]

bit_list1 = list(itertools.product([0, 1], repeat=len(former)))
bit_list2 = list(itertools.product([0, 1], repeat=len(latter)))

su1 = defaultdict(list)
su2 = defaultdict(list)

for bit in bit_list1:
    su,cnt = 0,0
    for i,b in enumerate(bit):
        if b:
            su += A[i]
            cnt += 1
    su1[cnt].append(su)

for bit in bit_list2:
    su,cnt = 0,0
    for i,b in enumerate(bit):
        if b:
            su += A[i]
            cnt += 1    
    su2[cnt].append(su)



ans = 0
for key in su1:
    if key > K:
        continue
    ans += 