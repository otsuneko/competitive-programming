N,M = map(int,input().split())
H = list(map(int,input().split()))
graph = [[] for _ in range(N)]
for _ in range(M):
    A,B = map(int,input().split())
    A,B = A-1,B-1
    graph[A].append(B)
    graph[B].append(A)

ans = 0
for i in range(N):
    h = H[i]
    flag = True

    for to in graph[i]:
        if h <= H[to]:
            flag = False
            break
    if flag:
        ans += 1
print(ans)