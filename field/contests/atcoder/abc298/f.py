from collections import defaultdict

N = int(input())

row = defaultdict(int)
col = defaultdict(int)
dic = defaultdict(int)

for _ in range(N):
    r,c,x = map(int,input().split())
    r,c = r-1,c-1
    row[r] += x
    col[c] += x
    dic[(r,c)] = x

rowl = []
for r in row:
    rowl.append((row[r],r))
rowl.sort(reverse=True)

coll = []
for c in col:
    coll.append((col[c],c))
coll.sort(reverse=True)


ans = 0
for nr,r in rowl:
    for nc,c in coll:
        if (r,c) in dic:
            ans = max(ans, nr+nc-dic[(r,c)])
        else:
            ans = max(ans, nr+nc)
            break

print(ans)