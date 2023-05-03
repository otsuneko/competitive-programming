#union-find木
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

#クラスカル法
# V: 頂点集合(リスト) E: 辺集合[始点, 終点, 重み](リスト)
class kruskal():
    def __init__(self, V, E):
        self.V = V
        self.E = E
        self.E.sort(key=lambda x: x[2]) #辺の重みでソート

    def weight(self): #最小全域木の重み和と選択された頂点を求める
        UF = UnionFind(len(self.V)) #頂点数でUnion Find Treeを初期化
        weight = 0
        nodes = set()
        edges = set()
        for i in range(len(self.E)):
            s,t,w = self.E[i]
            if not UF.same(s,t):
                UF.union(s,t)
                weight += w
                nodes.add(s)
                nodes.add(t)
                edges.add((s,t))

        return weight, sorted(list(nodes)), edges

N,M = map(int,input().split())
graph = [[] for _ in range(N)]
nodes = [0]*N # Vの要素数Nだけを使用
edges = []
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)
    edges.append((a,b,1))

mst = kruskal(nodes,edges)

print(M - len(mst.weight()[2]))