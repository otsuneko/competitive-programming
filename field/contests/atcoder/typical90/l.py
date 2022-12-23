from collections import defaultdict

class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n

    def find(self, x):
        if self.parents[x] < 0:
            return x
        else:
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

H,W = map(int,input().split())
masu = [[0]*W for i in range(H)]

uf = UnionFind(H*W)

Q = int(input())
for _ in range(Q):
    q = list(map(int,input().split()))
    if q[0] == 1:
        r,c = q[1]-1,q[2]-1
        masu[r][c] = 1

        move = ([1, 0], [-1, 0], [0, 1], [0, -1])
        for dy,dx in move:
            if 0 <= r+dy < H and 0 <= c+dx < W and masu[r+dy][c+dx] == 1:
                uf.union(c+r*W,(c+dx)+(r+dy)*W)

    elif q[0] == 2:
        r1,c1,r2,c2 = q[1]-1,q[2]-1,q[3]-1,q[4]-1
        if [masu[r1][c1],masu[r2][c2]] == [1,1]:
            print(["No","Yes"][uf.same(c1+r1*W, c2+r2*W)])
        else:
            print("No")