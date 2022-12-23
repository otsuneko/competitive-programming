N = int(input())
V = list(map(int,input().split()))
V.sort()

ans = V[0]
for i in range(1,N):
    ans = (ans+V[i])/2
print(ans)

