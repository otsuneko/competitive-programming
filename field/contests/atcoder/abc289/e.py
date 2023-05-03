from collections import deque
def bfs():
    queue = deque()
    queue.append((0,N-1,0))
    seen.add((0,N-1))
    while queue:
        taka,aoki,dist = queue.popleft()
        if taka == N-1 and aoki == 0:
            return dist
        for to1 in graph[taka]:
            for to2 in graph[aoki]:
                if C[to1] != C[to2] and (to1,to2) not in seen:
                    seen.add((to1,to2))
                    queue.append((to1,to2,dist+1))
    return -1

T = int(input())

for _ in range(T):
    N,M = map(int,input().split())
    C =  list(map(int,input().split()))
    graph = [[] for _ in range(N)]
    for _ in range(M):
        a,b = map(int,input().split())
        a,b = a-1,b-1
        graph[a].append(b)
        graph[b].append(a)

    seen = set()
    ans = bfs()
    print(ans)