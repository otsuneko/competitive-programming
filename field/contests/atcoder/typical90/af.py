import itertools
N = int(input())
A = [list(map(int,input().split())) for _ in range(N)]
M = int(input())
rumor = [list(map(int,input().split())) for _ in range(M)]

runner = [i for i in range(N)]
ptr = list(itertools.permutations(runner, N))
ans = float("INF")
for p in ptr:
    total = 0
    for i in range(N-1):
        for r in rumor:
            if [p[i]+1,p[i+1]+1] == r or [p[i+1]+1,p[i]+1] == r:
                break
        else:
            total += A[p[i]][i]
            continue
        break
    else:
        total += A[p[N-1]][N-1]
        ans = min(ans,total)
if ans == float("INF"):
    print(-1)
else:
    print(ans)