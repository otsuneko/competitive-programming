N,M = map(int,input().split())
A = list(map(int,input().split()))
B  = list(map(int,input().split()))

C = []
for i,a in enumerate(A):
    C.append((a,i))
for i,b in enumerate(B):
    C.append((b,i+N))

C.sort()

ansA = dict()
ansB = dict()

for i in range(N+M):
    n,idx = C[i]
    if idx < N:
        ansA[n] = i+1
    else:
        ansB[n] = i+1

ansA2 = []
ansB2 = []
for a in A:
    ansA2.append(ansA[a])
for b in B:
    ansB2.append(ansB[b])

print(*ansA2)
print(*ansB2)