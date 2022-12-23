N,M = map(int,input().split())
lamp = []
for _ in range(M):
    k, *switch = map(int,input().split())
    lamp.append(switch)
p = list(map(int,input().split()))

import itertools

ans = 0
for bit in itertools.product([True, False], repeat=N):

    for i in range(M):
        cnt = 0
        for s in lamp[i]:
            if bit[s-1] == 1:
                cnt += 1
        if cnt%2 != p[i]:
            break
    else:
        ans += 1
print(ans)