def is_ok(arg):
    x = 0
    cut = [0]
    for i in range(N):
        if A[i] - x >= arg:
            cut.append(A[i])
            x = A[i]
        if len(cut) == K+1:
            break

    cut.append(L)
    # print(arg,cut)

    if len(cut) != K+2:
        return False

    for i in range(len(cut)-1):
        l = cut[i+1]-cut[i]
        if l < arg:
            return False

    return True

def meguru_bisect(ng, ok):
    while (abs(ok - ng) > 1):
        mid = (ok + ng) // 2
        if is_ok(mid):
            ok = mid
        else:
            ng = mid
    return ok

N,L = map(int,input().split())
K = int(input())
A = list(map(int,input().split()))

ans = meguru_bisect(L,0)
print(ans)