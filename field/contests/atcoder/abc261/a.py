l1,r1,l2,r2 = map(int,input().split())

li = [0]*101
for i in range(l1,r1+1):
    li[i] += 1
for i in range(l2,r2+1):
    li[i] += 1

ans = 0
for i in range(l2,r2+1):
    if li[i] == 2:
        ans += 1
print(max(0,ans-1))
