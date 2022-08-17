N = int(input())
V = list(map(int,input().split()))

from collections import defaultdict
dict1 = defaultdict(int)
dict2 = defaultdict(int)

for i in range(N):
    if i%2==0:
        dict1[V[i]] += 1
    else:
        dict2[V[i]] += 1

# print(dict1,dict2)

ans = 0
ma1 = 0
for key in dict1:
    ma1 = max(ma1,dict1[key])

c1 = set()
for key in dict1:
    if dict1[key] == ma1:
        c1.add(key)

ma2 = 0
for key in dict2:
    ma2 = max(ma2,dict2[key])

c2 = set()
for key in dict2:
    if dict2[key] == ma2:
        c2.add(key)

if len(c1) == len(c2) == len(c1&c2) == 1:
    print(N//2)
else:
    print(N-ma1-ma2)