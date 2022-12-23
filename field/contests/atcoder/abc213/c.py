def compress(arr):
    *XS, = set(arr)
    XS.sort()
    return {e: i for i, e in enumerate(XS)}

H,W,N = map(int,input().split())
gyou = []
retsu = []
pos = []
for _ in range(N):
    A,B = map(int,input().split())
    gyou.append(A)
    retsu.append(B)
    pos.append((A,B))

gyou2 = compress(gyou)
retsu2 = compress(retsu)

for p in pos:
    print(gyou2[p[0]]+1,retsu2[p[1]]+1)
