from collections import defaultdict
import itertools

N,K =map(int,input().split())
S =[list(input()) for _ in range(N)]

ans = 0
for n in range(K,16):
    for cmb in itertools.combinations(S,n):
        dict = defaultdict(int)
        for s in cmb:
            for c in s:
                dict[c] += 1
        
        cnt = 0
        for key in dict:
            if dict[key] == K:
                cnt += 1
        
        ans = max(ans,cnt)

print(ans)