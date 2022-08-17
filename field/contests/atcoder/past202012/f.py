import itertools
N,M = map(int,input().split())
danger = [list(map(int,input().split())) for _ in range(M)]

import itertools
bit_list = list(itertools.product([0, 1], repeat=N))

ans = 0
for bit in bit_list:
    s = set([])
    b = set([i+1 for i in range(N) if bit[i] == 1])
    for d in danger:
        if len(set(d)-b) == 1:
            s.add(*(set(d)-b))
    ans = max(ans,len(s))

print(ans)