N = int(input())
H = list(map(int,input().split()))

ans = 0
cnt = 0
for i in range(N-2,-1,-1):
    if H[i] >= H[i+1]:
        cnt += 1
    else:
        ans = max(ans,cnt)
        cnt = 0
ans = max(ans,cnt)
print(ans)