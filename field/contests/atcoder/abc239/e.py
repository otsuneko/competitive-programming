# Pythonで提出!!
import sys
sys.setrecursionlimit(10**7)
from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right

N,Q =map(int,input().split())
X =list(map(int,input().split()))

graph = [[] for _ in range(N)]
for _ in range(N-1):
    a,b =map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)

def dfs(s,li):
    # 行きがけ
    li2 = []

    seen[s] = True
    for to in graph[s]:
        if seen[to]:
            continue
        insort(li2,X[to])
        if len(li2) > 20:
            li2 = li2[1:]
        li2 += dfs(to,li2)
        li2.sort()
        if len(li2) > 20:
            li2 = li2[len(li2)-20:]

    # 帰りがけ
    li3 = li2[:]
    insort(li3,X[s])
    dic[s] = li3

    return li2
    
seen = [False]*N
li = []
dic = dict()
dfs(0,li)
# print(dic)

for i in range(Q):
    v,k =map(int,input().split())
    v -= 1

    print(dic[v][-k])
