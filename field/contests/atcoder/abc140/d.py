from itertools import groupby
N,K = map(int,input().split())
S = list(input())

gr = groupby(S)
li = []
for k,v in gr:
    li.append(k)

l = len(li)
l -= 2*min(K,l//2)

if l == 0:
    print(N-1)
else:
    print(N-l)
