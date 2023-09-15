# import sys
# input = lambda: sys.stdin.readline().rstrip()
# INF = 10**18

# import sys
# sys.setrecursionlimit(10**7)

# def cycledetection(li):
#     s = set()
#     for i in range(len(li)):
#         if li[i] in s:
#               idx = li.index(li[i])
#               print(i-idx)
#               print(*li[idx:i])
#               exit()
#         s.add(li[i])

# N = int(input())
# A = list(map(int,input().split()))

# graph = [[] for _ in range(N+1)]
# for i in range(N):
#     a = i+1
#     b = A[i]
#     graph[a].append(b)

# seen = set()
# for i in range(N):
#     if i+1 in seen:
#         continue
#     li = [i+1]
#     seen.add(i+1)

#     while 1:
#         if A[li[-1]-1] not in seen:
#             seen.add(A[li[-1]-1])
#             li.append(A[li[-1]-1])
#         else:
#             li.append(A[li[-1]-1])
#             cycledetection(li)


N = int(input())
A = list(map(int,input().split()))

graph = [[] for _ in range(N)]
indeg = [0]*(N)
for i in range(N):
    a = i
    b = A[i]-1
    graph[a].append(b)
    indeg[b] += 1

from collections import deque
que = deque()
for i in range(N):
    if indeg[i] == 0:
        que.append(i)

while que:
    s = que.popleft()
    to = graph[s][0]
    indeg[to] -= 1
    if indeg[to] == 0:
        que.append(to)

s = indeg.index(1)
seen = set([s])
ans = [s+1]
while 1:
    to = graph[s][0]
    if to not in seen:
        seen.add(to)
        ans.append(to+1)
    else:
        break
    s = to

print(len(ans))
print(*ans)