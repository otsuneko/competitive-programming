def RunLengthEncoding(S):
    cur = S[0]
    cnt = 1
    res = []
    for i in range(1,len(S)):
        if cur == S[i]:
            cnt += 1
        else:
            res.append((cur,cnt))
            cur = S[i]
            cnt = 1
    res.append((cur,cnt))
    return res

N = int(input())
S = input()

res = RunLengthEncoding(S)

ans = -1
if len(res) == 1:
    print(ans)
    exit()
    
for c,n in res:
    if c == "o":
        ans = max(ans, n)

print(ans)