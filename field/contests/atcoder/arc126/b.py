N,M = map(int,input().split())
pos = []
to1 = dict()
to0 = dict()
for i in range(M):
    a,b = map(int,input().split())
    pos.append([a-1,b-1])
    to1[b-1] = a-1
    to0[a-1] = b-1

idx0 = idx1 = 0
while idx0 < N and idx1 < N:
    v0 = to0[idx0]
    v1 = to1[idx1]

    