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

N = int(input())
sx,sy,tx,ty = map(int,input().split())
circles =  [list(map(int,input().split())) for _ in range(N)]
uf = UnionFind(N)

for i,c1 in enumerate(circles):
    for j,c2 in enumerate(circles):
        if i == j:
            continue
        dist = (c1[0]-c2[0])**2 + (c1[1]-c2[1])**2
        if dist < (c1[2]-c2[2])**2 or dist > (c1[2]+c2[2])**2:
            continue
        uf.union(i,j)

sidx = set()
tidx = set()
for i,c in enumerate(circles):
    dist = (c[0]-sx)**2 + (c[1]-sy)**2
    if dist == c[2]**2:
        sidx.add(i)
    dist = (c[0]-tx)**2 + (c[1]-ty)**2
    if dist == c[2]**2:
        tidx.add(i)

for s in sidx:
    for t in tidx:
        if uf.same(s,t):
            print("Yes")
            exit()
print("No")