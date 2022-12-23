li = list(map(int,input().split()))
li.sort()

ans = 0
if li[0] != li[1]:
    diff = li[1]-li[0]
    li[1] -= diff
    li[2] -= diff
    ans += diff

if li[2] > li[1]*2:
    ans = -1
else:
    diff = li[2]-li[1]
    li[0] -= diff
    li[1] -= diff
    ans += diff*2
    if li[0] > 0:
        ans += li[0]

print(ans)
