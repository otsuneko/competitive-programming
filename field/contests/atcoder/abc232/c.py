import itertools


N,M = map(int,input().split())
ta = []
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    ta.append((a,b))
ao = set()
for _ in range(M):
    a,b = map(int,input().split())
    a,b = a-1,b-1
    ao.add((a,b))

seq = [i for i in range(N)]
ptr = list(itertools.permutations(seq))

for p in ptr:
    change = [0]*N
    for i,n in enumerate(p):
        change[i] = n

    cnt = 0
    for a,b in ta:
        c,d = change[a],change[b]
        if c > d:
            c,d = d,c
        if (c,d) in ao:
            cnt += 1
    
    if cnt == M:
        print("Yes")
        break
else:
    print("No")