import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18
    
N = int(input())
A = list(map(int,input().split()))
A2 = sorted(A)

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

rle = RunLengthEncoding(A2)
# print(rle)

cur = 0
from collections import defaultdict
dic = defaultdict(int)
for a,cnt in rle:
    cur += a*cnt
    dic[a] = cur
# print(dic)

ans = [0]*N
su = sum(A)
for i,a in enumerate(A):
    ans[i] = su-dic[a]
print(*ans)