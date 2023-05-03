N,A,B = map(int,input().split())
S = input()

ans = 10**18
for i in range(N):
    S2 = S[i%N:] + S[:i%N]
    diff_cnt = 0
    for j in range(N//2):
        if S2[j] != S2[N-1-j]:
            diff_cnt += 1

    ans = min(ans, A*i + B*diff_cnt)

print(ans)