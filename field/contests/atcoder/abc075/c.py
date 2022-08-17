from collections import defaultdict

class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1]*n

    def find(self, x):
        if self.parents[x] < 0:
            return x
        self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return

        if self.parents[x] > self.parents[y]:
            x, y = y, x

        self.parents[x] += self.parents[y]
        self.parents[y] = x

    def size(self, x):
        return -self.parents[self.find(x)]

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def members(self, x):
        root = self.find(x)
        return [i for i in range(self.n) if self.find(i) == root]

    def roots(self):
        return [i for i, x in enumerate(self.parents) if x < 0]

    def group_count(self):
        return len(self.roots())

    def all_group_members(self):
        group_members = defaultdict(list)
        for member in range(self.n):
            group_members[self.find(member)].append(member)
        return group_members

    def __str__(self):
        return '\n'.join(f'{r}: {m}' for r, m in self.all_group_members().items())
'''
uf = UnionFind(N) -> create 6 separated nodes
uf.union(0, 2) -> unite two ids
uf.same(0, 2) -> have same top node?
uf.find(0) -> id of top node
uf.size(5) -> num of group

# 文字列や任意の数字を要素にしたり復元したい場合
l = ['A', 'B', 'C', 'D', 'E']

# {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
d = {x: i for i, x in enumerate(l)}

# {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
d_inv = {i: x for i, x in enumerate(l)}

uf.union(d['A'], d['D'])
print(d_inv[uf.find(d['D'])])
# A
'''

N,M =map(int,input().split())
edge = []
for _ in range(M):
    a,b =map(int,input().split())
    a,b = a-1,b-1
    edge.append((a,b))

ans = 0
for i in range(M):
    uf = UnionFind(N)
    for j in range(M):
        if j == i:
            continue
        u,v = edge[j]
        uf.union(u,v)
    if uf.size(0) != N:
        ans += 1
print(ans)


###別解###
# import sys
# sys.setrecursionlimit(10**6)
# def bridge(adj, n):
#     result = set()
#     label = [None]*n
#     gen = 0
#     cost = [0]*n
#     def dfs(u, p):
#         nonlocal gen
#         res = 0
#         for v in adj[u]:
#             if v == p:
#                 continue
#             if label[v] is not None:
#                 if label[v] < label[u]:
#                     cost[v] += 1
#                     res += 1
#             else:
#                 label[v] = gen; gen += 1
#                 r = dfs(v, u)
#                 if r == 0:
#                     result.add((u, v) if u < v else (v, u))
#                 res += r
#         res -= cost[u]
#         return res
#     for v in range(n):
#         if not label[v]:
#             label[v] = gen; gen += 1
#             r = dfs(v, -1)
#             assert r == 0, r
#     return result

# N,M =map(int,input().split())
# graph = [[] for _ in range(N)]
# for _ in range(M):
#     a,b =map(int,input().split())
#     a,b = a-1,b-1
#     graph[a].append(b)
#     graph[b].append(a)

# ans = sorted(bridge(graph, N))
# print(len(ans))
