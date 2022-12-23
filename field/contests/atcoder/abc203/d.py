def is_ok(n):

    A2 = [[0]*N for _ in range(N)]
    for y in range(N):
        for x in range(N):
            if A[y][x] > n:
                A2[y][x] = 1
    # print(*A2, sep="\n")

    cumsum = [[0]*(N+1) for _ in range(N+1)]
    for y in range(N):
        for x in range(N):
            cumsum[y+1][x+1] = cumsum[y][x+1] + cumsum[y+1][x] - cumsum[y][x] + A2[y][x]
    # print(*cumsum, sep="\n")

    flag = False
    for y in range(N-K+1):
        for x in range(N-K+1):
            if cumsum[y+K][x+K] - cumsum[y+K][x] - cumsum[y][x+K] + cumsum[y][x] < K**2//2+1:
                flag = True

    return flag

def meguru_bisect(ng, ok):

    while (abs(ok - ng) > 1):
        mid = (ok + ng) // 2
        if is_ok(mid):
            ok = mid
        else:
            ng = mid
    return ok

N,K = map(int,input().split())

A = []
max_A = 0
for _ in range(N):
    tmp = list(map(int,input().split()))
    A.append(tmp)
    max_A = max(max_A, max(tmp))

ans = meguru_bisect(-1,max_A)
print(ans)