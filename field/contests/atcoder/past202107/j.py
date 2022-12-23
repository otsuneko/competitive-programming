import sys
sys.setrecursionlimit(10**7)

def detect_Cycle(v, visited, recStack):

    visited[v] = True
    recStack[v] = True

    for neighbour in graph[v]:
        if visited[neighbour] == False:
            if detect_Cycle(neighbour, visited, recStack) == True:
                return True
        elif recStack[neighbour] == True:
            return True

    recStack[v] = False
    return False

N,M = map(int,input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
    u,v = map(int,input().split())
    u,v = u-1,v-1
    graph[u].append(v)

visited = [False]*(N+1)
recStack = [False]*(N+1)
flag = False
for node in range(N):
    if visited[node] == False:
        if detect_Cycle(node,visited,recStack) == True:
            flag = True
            break

print(["No","Yes"][flag])