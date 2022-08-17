N = int(input())
X = list(map(int,input().split()))
X.sort()
mi,ma=X[0],X[-1]

ans = 10**18
for P in range(mi,ma+1):
    su = 0
    for j in range(N):
        su += (X[j]-P)**2
    ans = min(ans, su)
print(ans)