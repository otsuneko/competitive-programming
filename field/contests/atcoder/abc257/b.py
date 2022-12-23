N,K,Q = map(int,input().split())
A = list(map(int,input().split()))
L = list(map(int,input().split()))

pawn = [False]*N
for a in A:
    pawn[a-1] = True

for l in L:
    cnt = 0
    for i in range(N):
        if pawn[i]:
            cnt += 1
            if cnt == l:
                if i+1 == N:
                    continue
                elif pawn[i+1] != False:
                    continue
                else:
                    pawn[i],pawn[i+1] = False,True
                break

ans = []
for i,p in enumerate(pawn):
    if p:
        ans.append(i+1)
    
print(*ans)