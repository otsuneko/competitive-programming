K = int(input())

ans = 1
n = 7
for i in range(K+1):
    if n%K == 0:
        print(ans)
        exit()
    n = (n*10 + 7)%K
    ans += 1
print(-1)