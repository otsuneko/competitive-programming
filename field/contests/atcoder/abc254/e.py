from collections import deque

def bfs(x,k):
    ans = set([x])
    queue = deque()
    queue.append((x,0))
    while queue:
        s,n = queue.popleft()
        if n >= k:
            continue
        for to in graph[s]:
            if to in ans:
                continue
            ans.add(to)
            queue.append((to,n+1))
    return ans

N,M = map(int,input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

Q = int(input())
for _ in range(Q):
    x,k = map(int,input().split())
    ans = bfs(x-1,k)
    print(sum(ans) + len(ans))