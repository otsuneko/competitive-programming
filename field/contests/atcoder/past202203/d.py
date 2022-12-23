T,N =map(int,input().split())
P =[list(map(int,input().split())) for _ in range(T)]
ma = [0]*N
ans = 0
for p in P:
    for i in range(N):
        ma[i] = max(ma[i],p[i])
    print(sum(ma))