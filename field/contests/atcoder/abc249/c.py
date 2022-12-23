N,K = map(int,input().split())
S = [list(input()) for _ in range(N)]

from collections import defaultdict
import itertools

ans = 0
for i in range(1,N+1):
    for cmb in itertools.combinations(S,i):
        dict = defaultdict(int)
        for s in cmb:
            chrs = set(s)
            for c in chrs:
                dict[c] += 1
        
        cnt = 0
        for key in dict:
            if dict[key] == K:
                cnt += 1
        
        ans = max(ans,cnt)

print(ans)