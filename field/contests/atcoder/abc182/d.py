N = int(input())
A = list(map(int,input().split()))

ans = x = p = q = 0
for i in range(N):
    p += A[i]
    q = max(q,p)
    
    ans = max(ans, x+q)
    x = x + p
print(ans)