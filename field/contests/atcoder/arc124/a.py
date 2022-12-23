N,K = map(int,input().split())

cards = [-1]*N
pos = [[] for _ in range(N)]
for i in range(K):
    c,k = map(str,input().split())
    k = int(k)-1

    if c == "L":
        cards[k] = i+1
        for j in range(k+1,N):
            pos[j].append(i+1)
    else:
        cards[k] = i+1
        for j in range(k):
            pos[j].append(i+1)

ans = 1
for i in range(N):
    if cards[i] == -1:
        ans = ans*len(pos[i])%998244353
print(ans)