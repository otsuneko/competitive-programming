def sort_with_index(arr, reverse=False):
    if reverse:
        return sorted([ [x,i] for i, x in enumerate(arr)], reverse=True)
    else:
        return sorted([ [x,i] for i, x in enumerate(arr)])

N,M =map(int,input().split())
D =list(map(int,input().split()))

graph = [[] for _ in range(N)]
for _ in range(M):
    a,b =map(int,input().split())
    a,b = a-1,b-1
    graph[a].append(b)
    graph[b].append(a)
    D[a] -= 1
    D[b] -= 1

remain = sort_with_index(D)
# print(remain)

l = 0
r = N-1
for n,i in remain:
    if n == 0:
        l += 1
    else:
        break

ans = []
while l < r:
    ans.append((remain[l][1]+1,remain[r][1]+1))
    remain[l][0] -= 1
    remain[r][0] -= 1
    
    if remain[l][0] == 0:
        l += 1
    if remain[r][0] > 0:
        ans.append((remain[r][1]+1,remain[r-1][1]+1))
        remain[r][0] -= 1
        remain[r-1][0] -= 1
        if remain[r][0] == 0:
            r -= 1
    else:
        r -= 1

for n,i in remain:
    if n != 0:
        print(-1)
        exit()

for a in ans:
    print(*a)
