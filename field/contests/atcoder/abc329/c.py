import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
S = input()

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

rle = RunLengthEncoding(S)
# print(rle)

ans = set()
for key,val in rle:
    for i in range(1,val+1):
        ans.add((key,i))
print(len(ans))