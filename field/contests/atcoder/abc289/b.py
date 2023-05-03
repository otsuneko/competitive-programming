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

N,M = map(int,input().split())
A = list(map(int,input().split()))
uf = UnionFind(N+1)
for a in A:
    uf.union(a,a+1)

seen = set()
ans = []
for i in range(1,N+1):
    if i in seen:
        continue
    li = uf.members(i)
    ans += sorted(li, reverse=True)
    seen |= set(li)
print(*ans)

# # Pythonで提出!!
# import sys
# sys.setrecursionlimit(10**7)

# ans = []
# def dfs(s):
#     seen.add(s)
#     for to in graph[s]:
#         dfs(to)
#     ans.append(s+1)

# N,M = map(int,input().split())
# A = list(map(int,input().split()))
# graph = [[] for _ in range(N)]
# for a in A:
#     graph[a-1].append(a)

# seen = set()
# for i in range(N):
#     if i not in seen:
#         dfs(i)
# print(*ans)