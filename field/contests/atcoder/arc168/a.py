import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

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
rle = RunLengthEncoding(S)

ans = 0
for key,val in rle:
    if key == ">":
        ans += val*(val+1)//2

print(ans)
