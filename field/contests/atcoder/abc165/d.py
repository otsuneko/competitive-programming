import time
A,B,N = map(int,input().split())

start = time.time()

x = min(N,B-1)
ans = 0
while x <= N:
    now = time.time()
    if now-start > 1.9:
        break
    ans = max(ans, (A*x)//B - A * (x//B))
    x += B
print(ans)