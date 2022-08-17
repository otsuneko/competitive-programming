def compress(arr):
    *XS, = set(arr)
    XS.sort()
    return {e: i for i, e in enumerate(XS)}

N,M = map(int,input().split())
city = []
pref = [[] for _ in range(N)]
for i in range(M):
    P,Y = map(int,input().split())
    city.append((P,Y))
    pref[P-1].append(Y)

comp_city = {}
for p in pref:
    comped = compress(p)
    comp_city.update(comped)

for c in city:
    ans = str(c[0]).zfill(6) + str(comp_city[c[1]]+1).zfill(6)
    print(ans)