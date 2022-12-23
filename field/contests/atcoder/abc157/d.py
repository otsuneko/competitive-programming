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

N,M,K = map(int,input().split())
uf = UnionFind(N)

direct_friend = [[] for _ in range(N)]
block = []

for _ in range(M):
    A,B = map(int,input().split())
    A,B = A-1,B-1
    direct_friend[A].append(B)
    direct_friend[B].append(A)
    uf.union(A,B)

for _ in range(K):
    C,D = map(int,input().split())
    C,D = C-1,D-1
    block.append([C,D])

ans = [0]*N
for i in range(N):
    # 交友関係リンクの中にいる人数のうち、自分及び自分と直接の交友関係にある者を除いた人数
    ans[i] = uf.size(i)-1 - len(direct_friend[i])

for C,D in block:
    # 交友関係リンクの中にいるペアのうち、直接の交友関係はないがブロック関係にあるものは除く
    if uf.same(C,D) and direct_friend[C].count(D) == 0:
        ans[C] -= 1
        ans[D] -= 1

print(*ans)