from collections import deque
from collections import defaultdict

full = set([i for i in range(9)])
def bfs():
    queue = deque()
    queue.append(tuple(s_pat))
    pattern[tuple(s_pat)] = 0

    while queue:
        s = queue.popleft()
        blank = list(full - set(s))[0]
        for to in graph[blank]:
            tmp = list(s)
            idx = tmp.index(to)
            tmp[idx] = blank
            if pattern[tuple(tmp)] > 0 or tmp == s_pat:
                continue
            pattern[tuple(tmp)] = pattern[s] + 1
            queue.append(tuple(tmp))

M = int(input())

graph = [[] for _ in range(9)]
for i in range(M):
    u,v = map(int, input().split())
    u,v = u-1,v-1
    graph[u].append(v)
    graph[v].append(u)

pattern = defaultdict(int)

s_pat = list(map(int,input().split()))
s_pat = [i-1 for i in s_pat]
bfs()
# for p in pattern:
#     print(p, pattern[p])

f_pat = [i for i in range(8)]
if pattern[tuple(f_pat)] > 0 or s_pat == f_pat:
    print(pattern[tuple(f_pat)])
else:
    print(-1)