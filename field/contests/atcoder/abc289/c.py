N,M = map(int,input().split())

nums = []
for _ in range(M):
    C = int(input())
    A = set(list(map(int,input().split())))
    nums.append(A)

import itertools

ans = 0
for bit in itertools.product([True, False], repeat=M):
    s = set()
    for i,b in enumerate(bit):
        if b:
            s |= nums[i]
    
    if len(s) == N:
        ans += 1
print(ans)