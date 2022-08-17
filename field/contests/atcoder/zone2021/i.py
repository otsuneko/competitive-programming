import itertools
N,M = map(int,input().split())

graph = [[] for i in range(N)]
for i in range(M):
    s,t = map(int,input().split())
    graph[s].append(t)
    graph[t].append(s)

l = [i for i in range(N)]
cmb = list(itertools.combinations(l,3)) # 組み合わせ列挙 5C3

ans_list = []
max_l = 0
for c in cmb:
    s = set([])
    for i in c:
        s.add(i)
        for v in graph[i]:
            s.add(v)
    print(c,s,len(s))
    if len(s) > max_l:
        max_l = len(s)
        ans_list = c

print(*ans_list)