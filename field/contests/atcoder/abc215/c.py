S,K = map(str,input().split())

import itertools
S2 = sorted(list(S))
ptr = list(itertools.permutations(S2, len(S))) #順列列挙 5P3

ans = []
check = set()
for p in ptr:
    # print(p)
    if p not in check:
        ans.append(p)
        check.add(p)

print("".join(ans[int(K)-1]))