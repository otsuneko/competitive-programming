from collections import deque
N,Q = map(int,input().split())
graph_asc = [[] for _ in range(N)]
graph_desc = [[] for _ in range(N)]
for _ in range(Q):
    query = list(map(int,input().split()))

    if query[0] == 1:
        x,y = query[1]-1,query[2]-1
        graph_asc[x].append(y)
        graph_desc[y].append(x)
    elif query[0] == 2:
        x,y = query[1]-1,query[2]-1
        graph_asc[x].pop()
        graph_desc[y].pop()
    elif query[0] == 3:
        x = query[1]-1
        ans = deque([x])
        cur = x
        while 1:
            if len(graph_asc[cur]) > 0:
                cur = graph_asc[cur][0]
                ans.append(cur)
            else:
                break
        cur = x
        while 1:
            if len(graph_desc[cur]) > 0:
                cur = graph_desc[cur][0]
                ans.appendleft(cur)
            else:
                break
        
        ans = [i+1 for i in ans]
        print(len(ans), *ans)
