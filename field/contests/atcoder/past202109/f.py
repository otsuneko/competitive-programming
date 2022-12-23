N = int(input())
S = list(input())
P = [-1]*N
unused = []
for i in range(N):
    if S[i] == "1":
        P[i] = i+1
    else:
        unused.append(i+1)

idx = 1
for i in range(N):
    if P[i] == -1 and unused[idx%len(unused)] != i+1:
        P[i] = unused[idx%len(unused)]
        idx += 1

for p in P:
    if p == -1:
        print(-1)
        break
else:
    print(*P)