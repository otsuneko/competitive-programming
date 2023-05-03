S = input()

ans = ""
for i in range(len(S)):
    if S[i] == "0":
        ans += "1"
    else:
        ans += "0"
print(ans)