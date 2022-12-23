H,W = map(int,input().split())
S = [list(input()) for _ in range(H)]

ans = 0
for h in range(H):
    ans += S[h].count("#")

print(ans)