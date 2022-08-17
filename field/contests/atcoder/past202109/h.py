from collections import deque
import sys
sys.setrecursionlimit(10**9)

def dfs(s,total_cost, path,seen):
    for to,cost in graph[s]:
        if seen[to] == False:
            if total_cost + cost == X:
                print("Yes")
                exit()
            elif total_cost + cost < X:
                seen[to] = True
                path.append(cost)
                dfs(to, total_cost + cost, path, seen)
                path.pop()
                seen[to] = False
            else:
                sub = []
                while total_cost + cost >= X and path:
                    tmp_cost = path.popleft()
                    sub.append(tmp_cost)
                    total_cost -= tmp_cost
                    if total_cost + cost == X:
                        print("Yes")
                        exit()
                seen[to] = True
                path.append(cost)
                dfs(to, total_cost + cost, path, seen)
                path.pop()
                seen[to] = False
                for tmp_cost in sub[::-1]:
                    total_cost += tmp_cost
                    path.appendleft(tmp_cost)

N,X = map(int, input().split())

graph = [[] for _ in range(N)]
for i in range(N-1):
 a,b,d = map(int, input().split())
 a,b = a-1,b-1
 graph[a].append((b,d))
 graph[b].append((a,d))

s_list = []
for i in range(N):
    if len(graph[i]) == 1:
        s_list.append(i)

for s in s_list:
    path = deque()
    seen = [False]*N
    seen[s] = True
    dfs(s,0,path,seen)
print("No")