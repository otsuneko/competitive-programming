import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

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

N,Q = map(int,input().split())
uf = UnionFind(N)

from collections import defaultdict
dic = defaultdict(set)

for _ in range(Q):
    t,*q = map(int,input().split())
    if t == 1:
        u,v = q
        u,v = u-1,v-1
        uf.union(u,v)
        root = uf.find(u)
        if len(dic[root]) > len(dic[u]):
            dic[root] |= dic[u]
        else:
            dic[u] |= dic[root]
            dic[root] = dic[u]
        if len(dic[root]) > len(dic[v]):
            dic[root] |= dic[v]
        else:
            dic[v] |= dic[root]
            dic[root] = dic[v]
        dic[root].add(u)
        dic[root].add(v)
    elif t == 2:
        v,k = q
        v -= 1
        if uf.size(v) < k:
            print(-1)
        else:
            root = uf.find(v)
            li = sorted(list(dic[v]),reverse=True)
            if len(li) == 0:
                print(v+1)
            else:
                print(li[k-1]+1)
