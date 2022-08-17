import sys
sys.setrecursionlimit(10**7)

def dfs(s,seen):

    path.append(s)

    if seen[s]:
        return s,len(path)-1

    seen[s] = True

    return dfs(A[s-1],seen)

N,K = map(int,input().split())
A = list(map(int,input().split()))

seen = [False]*(N+1)
path = []
n,end = dfs(1,seen)
loop_start = path.index(n)
if K < loop_start:
    ans = path[K]
else:
    K -= loop_start
    ans = path[loop_start + K%(end-loop_start)]
print(ans)