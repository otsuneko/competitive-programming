import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

# 重み付きUnionFind
class WeightedUnionFind:
    def __init__(self, n):
        self.parents = [i for i in range(n)] # 親
        self.rank = [0]*n # 木の深さ
        self.weights = [0]*n # 重み

    # xの根を探索
    def find(self, x):
        if self.parents[x] == x:
            return x
        root = self.find(self.parents[x])
        self.weights[x] += self.weights[self.parents[x]]
        self.parents[x] = root
        return root

    # xからyへの重みをweightとして統合
    def union(self, x, y, weight=0):
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            self.parents[root_x] = root_y
            self.weights[root_x] = weight - self.weights[x] + self.weights[y]
        else:
            self.parents[root_y] = root_x
            self.weights[root_y] = -weight - self.weights[y] + self.weights[x]
            if self.rank[root_x] == self.rank[root_y]:
                self.rank[root_x] += 1
        return True

    # xとyが同じグループか
    def same(self, x, y):
        return self.find(x) == self.find(y)

    # xからyへのコスト
    def diff(self, x, y):
        return self.weights[x] - self.weights[y]

'''
wuf = WeightedUnionFind(N) -> create N separated nodes
wuf.union(0, 2, 5) -> unite two ids with weight=5 from 0 to 2
wuf.same(0, 2) -> have same top node?
wuf.find(0) -> id of top node

# 文字列や任意の数字を要素にしたり復元したい場合
l = ['A', 'B', 'C', 'D', 'E']

# {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
d = {x: i for i, x in enumerate(l)}

# {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
d_inv = {i: x for i, x in enumerate(l)}

wuf.union(d['A'], d['D'], weight)
print(d_inv[uf.find(d['D'])])
# A
'''

N,Q = map(int,input().split())

uf = WeightedUnionFind(N)
ans = []
for i in range(Q):
    a,b,d = map(int,input().split())
    a,b = a-1,b-1
    if uf.union(a,b,d):
        ans.append(i+1)
    elif uf.diff(a,b) == d:
        ans.append(i+1)
print(*ans)