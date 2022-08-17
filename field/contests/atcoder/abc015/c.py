N,K =map(int,input().split())
T =[list(map(int,input().split())) for _ in range(N)]

vals = set(T[0])
for i in range(1,N):
    tmp = set()
    for v in vals:
        for k in range(K):
            tmp.add(v^T[i][k])
    vals = tmp

if 0 in vals:
    print("Found")
else:
    print("Nothing")