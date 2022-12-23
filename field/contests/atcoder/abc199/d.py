from collections import deque

def solve():
    seen = [False for i in range(n+1)]
    ans = 1
    for i in range(1,n+1):
        if seen[i]:
            continue
        cnt = 0
        for v in graph[i]:
            cnt += 1
            seen[v] = True
        if cnt == 0:
            ans *= 3
            continue
        elif cnt >= 3:
            return 0
        else:
            ans *= 6
    return ans

n, m = map(int, input().split())

graph = [[] for _ in range(n+1)]
for i in range(m):
 a, b = map(int, input().split())
 graph[a].append(b)
 graph[b].append(a)

print(solve())