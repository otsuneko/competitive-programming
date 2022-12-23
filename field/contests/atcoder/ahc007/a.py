#union-find木
class UnionFind:
    def __init__(self, n):
        self.par = [i for i in range(n)] #親
        self.rank = [0 for _ in range(n)] #根の深さ

    #xの属する木の根を求める
    def find(self, x):
        if self.par[x] == x:
            return x
        else:
            self.par[x] = self.find(self.par[x])
            return self.par[x]

    #xとyの属する集合のマージ
    def unite(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return
        if self.rank[x] < self.rank[y]:
            self.par[x] = y
        else:
            self.par[y] = x
            if self.rank[x] == self.rank[y]:
                self.rank[x] += 1

    #xとyが同じ集合に属するかを判定
    def same(self, x, y):
        return self.find(x) == self.find(y)


#クラスカル法
# V: 頂点集合(リスト) E: 辺集合[始点, 終点, 重み](リスト)
class kruskal():
    def __init__(self, V, E):
        self.V = V
        self.E = E
        self.E.sort(key=lambda x: x[2]) #辺の重みでソート

    def weight(self): #最小全域木の重み和を求める
        UF = UnionFind(len(V)) #頂点数でUnion Find Treeを初期化
        res = 0
        for i in range(len(self.E)):
            e = self.E[i]

            if (UF.same(e[0], e[1])) == False:
                UF.unite(e[0], e[1])
                res += e[2]

        return res

    def edge(self):
        UF = UnionFind(len(self.V)) #頂点数でUnion Find Treeを初期化
        res_E = []
        for i in range(len(self.E)):
            e = self.E[i]

            if (UF.same(e[0], e[1])) == False:
                UF.unite(e[0], e[1])
                res_E.append(e)

        return res_E

    def node(self):
        UF = UnionFind(len(V)) #頂点数でUnion Find Treeを初期化
        res_V = []
        for i in range(len(E)):
            e = E[i]

            if (UF.same(e[0], e[1])) == False:
                UF.unite(e[0], e[1])
                res_V.append(e[0])
                res_V.append(e[1])

        return list(set(res_V))


N,M = 400,1995
V = [0]*N # Vの要素数Nだけを使用
E = []
pos = [list(map(int,input().split())) for _ in range(N)]
edges = []
for _ in range(M):
    u,v = map(int,input().split())
    x1,y1 = pos[u]
    x2,y2 = pos[v]
    dist = ((x1-x2)**2 + (y1-y2)**2)
    E.append((u,v,dist))
    edges.append((u,v))

#kNN
knn = [set() for _ in range(N)]
import heapq  # heapqライブラリのimport
for i in range(N):
    posl = []
    x1,y1 = pos[i]
    for j in range(N):
        if i==j:
            continue
        x2,y2 = pos[j]
        heapq.heappush(posl, ( (x1-x2)**2+(y1-y2)**2, j))

    tmp = heapq.nsmallest(5,posl)
    for t in tmp:
        knn[i].add(t[1])

k = kruskal(V,E)
li = k.edge()

use_edges = set()
for u,v,w in li:
    use_edges.add((u,v))

unused = set()
seen = set()
for i,edge in enumerate(edges):

    l = int(input())

    u,v = edge
    x1,y1 = pos[u]
    x2,y2 = pos[v]
    dist = int(((x1-x2)**2 + (y1-y2)**2)**0.5)

    if l > dist*2.5 and i < 1500:
        if u not in seen:
            unused.add(u)
        else:
            unused.add(v)
        if u not in seen and v in knn[u]:
            print(1,flush=True)
            seen.add(u)
            seen.add(v)
        else:
            print(0,flush=True)
    elif edge in use_edges:
        print(1,flush=True)
        seen.add(u)
        seen.add(v)