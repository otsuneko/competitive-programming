N = int(input())
pos = [list(map(int,input().split())) for _ in range(N)]

li = [i for i in range(1,N)]

import itertools

ans = 10**18
for ptr in itertools.permutations(li):
    cost = 0
    ptr = [0] + list(ptr) + [0]
    for i in range(1,len(ptr)):
        x,y,z = pos[ptr[i]]
        px,py,pz = pos[ptr[i-1]]
        cost += abs(x-px) + abs(y-py) + max(z-pz,0)
    ans = min(ans,cost)
print(ans)