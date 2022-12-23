N = int(input())
S = input()
W = list(map(int,input().split()))

from collections import defaultdict
dict = defaultdict(list)
for i in range(N):
    if dict[W[i]]:
        if S[i] == "0":
            dict[W[i]][1] += 1
        else:
            dict[W[i]][0] += 1
    else:
        if S[i] == "0":
            dict[W[i]] = [0,1]
        else:
            dict[W[i]] = [1,0]

ans = cnt = S.count("1")
keys = list(dict.keys())
keys.sort()

for key in keys:
    cnt += dict[key][1] - dict[key][0]
    ans = max(ans,cnt)
print(ans)