S = input()

ans = 10**18
cnt = 0
for i in range(len(S)):
    if i%2:
        if S[i] == "0":
            cnt += 1
    else:
        if S[i] == "1":
            cnt += 1
ans = min(ans, cnt)

cnt = 0
for i in range(len(S)):
    if i%2:
        if S[i] == "1":
            cnt += 1
    else:
        if S[i] == "0":
            cnt += 1
ans = min(ans, cnt)
print(ans)