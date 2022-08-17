N,K = map(int,input().split())

ans = 0
for i in range(N):
    for j in range(K):
        s = str(i+1)+"0"+str(j+1)
        ans += int(s)
print(ans)