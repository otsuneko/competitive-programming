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

N,M,E = map(int,input().split())
edge = []
for _ in range(E):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    edge.append((a,b))

Q = int(input())
X = []
for _ in range(Q):
    x = int(input())
    x -= 1
    X.append(x)

ini_X = set([i for i in range(E)]) - set(X)
uf = UnionFind(N+M)
light_sum = 0
unlighted = [1]*N + [0]*M
for x in ini_X:
    u,v = edge[x]
    if uf.same(u,v):
        continue
    # u,vが両方都市
    if 0 <= u < v < N:
        # u,vのどちらかがok、どちらかがngならlight_sum++
        if unlighted[uf.find(u)] and not unlighted[uf.find(v)]:
            uid = uf.find(u)
            vid = uf.find(v)
            uf.union(u,v)
            nid = uf.find(u)
            light_sum += unlighted[uid]
            unlighted[uid] = unlighted[vid] = unlighted[nid] = 0
        elif (unlighted[uf.find(v)] and not unlighted[uf.find(u)]):
            uid = uf.find(u)
            vid = uf.find(v)
            uf.union(u,v)
            nid = uf.find(u)
            light_sum += unlighted[vid]
            unlighted[uid] = unlighted[vid] = unlighted[nid] = 0
        # u,vの両方がng
        if (unlighted[uf.find(u)] and unlighted[uf.find(v)]):
            uid = uf.find(u)
            vid = uf.find(v)
            uf.union(u,v)
            nid = uf.find(u)
            if uid == nid:
                unlighted[nid] += unlighted[vid]
                unlighted[vid] = 0
            elif vid == nid:
                unlighted[nid] += unlighted[uid]
                unlighted[uid] = 0
            
    # uが都市、vが発電所
    elif u < N and N <= v:
        # uがngならlighted++
        uid = uf.find(u)
        vid = uf.find(v)
        uf.union(u,v)
        nid = uf.find(u)
        if unlighted[uid]:
            light_sum += unlighted[uid]
            unlighted[uid] = 0


# print(ini_X)
# print(lighted)

ans = [0]*Q
for i in range(Q-1,-1,-1):
    ans[i] = light_sum
    u,v = edge[X[i]]
    if uf.same(u,v):
        continue
    # u,vが両方都市
    if 0 <= u < v < N:
        # u,vのどちらかがok、どちらかがngならlight_sum++
        if unlighted[uf.find(u)] and not unlighted[uf.find(v)]:
            uid = uf.find(u)
            vid = uf.find(v)
            uf.union(u,v)
            nid = uf.find(u)
            light_sum += unlighted[uid]
            unlighted[uid] = unlighted[vid] = unlighted[nid] = 0
        elif (unlighted[uf.find(v)] and not unlighted[uf.find(u)]):
            uid = uf.find(u)
            vid = uf.find(v)
            uf.union(u,v)
            nid = uf.find(u)
            light_sum += unlighted[vid]
            unlighted[uid] = unlighted[vid] = unlighted[nid] = 0
        # u,vの両方がng
        if (unlighted[uf.find(u)] and unlighted[uf.find(v)]):
            uid = uf.find(u)
            vid = uf.find(v)
            uf.union(u,v)
            nid = uf.find(u)
            if uid == nid:
                unlighted[nid] += unlighted[vid]
                unlighted[vid] = 0
            elif vid == nid:
                unlighted[nid] += unlighted[uid]
                unlighted[uid] = 0
            
    # uが都市、vが発電所
    elif u < N and N <= v:
        # uがngならlighted++
        uid = uf.find(u)
        vid = uf.find(v)
        uf.union(u,v)
        nid = uf.find(u)
        if unlighted[uid]:
            light_sum += unlighted[uid]
            unlighted[uid] = 0

for a in ans:
    print(a)