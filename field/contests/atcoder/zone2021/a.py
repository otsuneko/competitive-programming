S = input()

ans = 0
for i in range(len(S)):
    if S[i:i+4] == "ZONe":
        ans += 1
print(ans)