S1 = input()
S2 = input()
S3 = input()
T = list(input())

ans = ""
for t in T:
    if t == "1":
        ans += S1
    elif t == "2":
        ans += S2
    else:
        ans += S3
print(ans)