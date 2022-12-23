Q =int(input())
from collections import deque
d = deque()
for _ in range(Q):
    query = list(map(int,input().split()))
    
    if query[0] == 1:
        x,c = query[1:]
        d.append([x,c])
    elif query[0] == 2:
        c = query[1]
        ans = 0
        while c > 0:
            if d[0][1] > c:
                ans += d[0][0]*c
                d[0][1] -= c
                c = 0
            elif d[0][1] == c:
                ans += d[0][0]*c
                d.popleft()
                c = 0
            else:
                ans += d[0][0]*d[0][1]
                c -= d[0][1]
                d.popleft()
        print(ans)