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

    def edge(self,ans):
        UF = UnionFind(len(self.V)) #頂点数でUnion Find Treeを初期化
        res_E = []
        for i in range(len(self.E)):
            e = self.E[i]
            if e[3] >= M:
                if UF.same(e[0], e[1]):
                    ans[e[3]-M] = "No"
                else:
                    ans[e[3]-M] = "Yes"
            else:
                UF.unite(e[0], e[1])
                res_E.append(e)

        return ans

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

N,M,Q =map(int,input().split())
V = [0]*N # Vの要素数Nだけを使用
E = []
for _ in range(M):
    a,b,c =map(int,input().split())
    a,b = a-1,b-1
    E.append((a,b,c,len(E)))

for _ in range(Q):
    u,v,w =map(int,input().split())
    u,v = u-1,v-1
    E.append((u,v,w,len(E)))

from collections import defaultdict
ans = ["No"]*Q
k = kruskal(V,E)
ans = k.edge(ans)

for a in ans:
    print(a)