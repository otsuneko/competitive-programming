import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,M = map(int,input().split())
S = input()
C = list(map(int,input().split()))

from collections import defaultdict
dic = defaultdict(list)

for i,s in enumerate(S):
    dic[C[i]].append(s)
# print(dic)

cnt = [0]*len(dic.keys())

ans = []
for i,s in enumerate(S):
    c = dic[C[i]][-1 + cnt[C[i]-1]]
    ans.append(c)
    cnt[C[i]-1] += 1
print("".join(ans))