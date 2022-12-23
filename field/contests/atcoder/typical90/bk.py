from collections import defaultdict
import itertools
H,W =map(int,input().split())
P =[list(map(int,input().split())) for _ in range(H)]

cmb = []
for i in range(1,H+1):
    cmb += list(itertools.combinations(P,i))

ans = 0
for c in cmb:
    row = len(c)
    col = len(c[0])
    inv = list(zip(*c))    
    cnt = defaultdict(int)
    for i in range(col):
        if len(set(inv[i])) == 1:
            cnt[inv[i][0]] += 1
    
    ma = 0
    for key in cnt:
        ma = max(ma, cnt[key])
    
    ans = max(ans, row * ma)

print(ans)