N,K = map(int,input().split())
S = input()

ans = ""
cnt = 1
for i in range(N):
    if cnt <=K and S[i] == "o":
        ans += "o"
        cnt += 1
    else:
        ans += "x"
print(ans)