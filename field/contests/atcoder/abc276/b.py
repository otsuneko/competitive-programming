from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right

N,M = map(int,input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    insort(graph[a],b+1)
    insort(graph[b],a+1)

for i in range(N):
    print(len(graph[i]),*graph[i])