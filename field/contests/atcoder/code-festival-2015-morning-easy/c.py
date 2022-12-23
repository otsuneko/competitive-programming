N,K,M,R = map(int,input().split())
S = [int(input()) for _ in range(N-1)]
S.sort(reverse=True)

ans = 0
if K == N:
    ans = max(0,N*R-sum(S))
    if ans > M:
        ans = -1
else:
    if sum(S[:K])/K >= R:
        ans = 0
    else:
        ans = max(0,K*R - sum(S[:K-1]))
        if ans > M:
            ans = -1
print(ans)