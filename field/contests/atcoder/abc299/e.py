from collections import deque

def bfs(s,d):
    queue = deque()
    queue.append(s)
    dist[s] = 0

    if d == 0:
        if S[s] == "0":
            print("No")
            exit()
        else:
            return

    cnt = 0
    while queue:
        s = queue.popleft()
        if dist[s] > d:
            break
        elif dist[s] == d:
            if S[s] == "1":
                cnt += 1
                continue
        S[s] = "0"

        for to in graph[s]:
            if dist[to] != -1:
                continue
            dist[to] = dist[s] + 1
            if dist[to] < d:
                S[to] = "0"
            queue.append(to)

    if cnt == 0:
        print("No")
        exit()

N,M = map(int,input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

S = ["1"]*N
K = int(input())
for _ in range(K):
    p,d = map(int,input().split())
    p -= 1

    dist = [-1]*N
    bfs(p,d)

if S.count("1") == 0:
    print("No")
else:
    print("Yes")
    print("".join(S))