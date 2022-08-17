S = list(input())

ans = []
for s in S[::-1]:
    if s == "6":
        ans.append("9")
    elif s == "9":
        ans.append("6")
    else:
        ans.append(s)
print("".join(ans))
