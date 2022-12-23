N =int(input())
A =list(map(int,input().split()))

li = [0,360]
total = 0
for i in range(N):
    total += A[i]
    li.append(total%360)

li.sort()
ans = 0
for i in range(N+1):
    ans = max(ans, li[i+1]-li[i])
print(ans)