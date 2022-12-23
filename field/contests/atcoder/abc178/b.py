a,b,c,d = map(int,input().split())

ab = [a,b]
cd = [c,d]

ans = -10**18-1
for x in ab:
    for y in cd:
        ans = max(ans, x*y)
print(ans)