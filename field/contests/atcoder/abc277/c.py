N = int(input())
from collections import defaultdict
dict = defaultdict(list)

for _ in range(N):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    dict[a].append(b)
    dict[b].append(a)

ans = 1
from collections import deque
d = deque([0])
seen = set([0])
while d:
    q = d.popleft()
    for floor in dict[q]:
        if floor in seen:
            continue
        d.append(floor)
        ans = max(ans,floor+1)
        seen.add(floor)
    
print(ans)