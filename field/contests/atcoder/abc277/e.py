from collections import deque

def bfs_01(s):
    # 最初はスイッチオフからスタート
    que = deque([[s,0]])
    while que:
        s,flg = que.popleft()
        if s == N-1:
            print(dist[flg][N-1])
            exit()

        li = [0]
        if s in switches:
            li = [0,1]
        for i in li:
            for to, w in graph[(flg+i)%2][s]:
                d = dist[flg][s] + w
                if d < dist[(flg+i)%2][to]:
                    dist[(flg+i)%2][to] = d
                    que.append((to,(flg+i)%2))

N,M,K = map(int,input().split())
graph = [[[] for _ in range(N)] for _ in range(2)]

for _ in range(M):
    u,v,a = map(int,input().split())
    u,v = u-1,v-1
    if a == 0:
        # はじめ通行不能
        graph[1][u].append((v,1))
        graph[1][v].append((u,1))
    elif a == 1:
        # はじめ通行可能
        graph[0][u].append((v,1))
        graph[0][v].append((u,1))

switches = list(map(int,input().split()))
for i in range(K):
    switches[i] -= 1
switches = set(switches)

dist = [[10**9]*N for _ in range(2)]
dist[0][0] = 0
bfs_01(0)
print(-1)
