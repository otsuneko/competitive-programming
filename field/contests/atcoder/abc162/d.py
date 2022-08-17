N = int(input())
S = list(input())

cnt = [{"R":0,"G":0,"B":0} for _ in range(N+1)]
color = {"R","G","B"}

# iより後ろにあるRGBの数
for i in range(N-1,-1,-1):
    for c in color:
        cnt[i][c] = cnt[i+1][c]
    cnt[i][S[i]] += 1

# 3色の組み合わせを全列挙
ans = 0
for i in range(N):
    for j in range(i+1,N):
        if S[i] != S[j]:
                c = color - {S[i],S[j]}
                ans += cnt[j+1][list(c)[0]]

# 3色の組み合わせのうちj-i = k-jの数
sub = 0
for i in range(N):
    for j in range(i+1,N):
        if S[i] != S[j]:
            if j + (j-i) < N and S[j + (j-i)] not in [S[i],S[j]]:
                sub += 1

print(ans-sub)