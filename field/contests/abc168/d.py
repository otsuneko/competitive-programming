import networkx as nx
n,m=map(int,input().split())
s=[list(map(int,input().split())) for i in range(m)]
 
g=nx.Graph()
g.add_nodes_from([i for i in range(1,n+1)])
 
for x in s:
    g.add_edge(x[0],x[1])
di=nx.predecessor(g,source=1)

if len(di)!=n:
    print("No")
    exit()
 
print("Yes")
for x in range(2,n+1):
    print(di[x][0])



