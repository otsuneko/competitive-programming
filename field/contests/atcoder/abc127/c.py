N,M = map(int,input().split())
l,r = 0,10**5+1

for _ in range(M):
    L,R = map(int,input().split())
    l = max(l,L)
    r = min(r,R)
print(max(0,r-l+1))