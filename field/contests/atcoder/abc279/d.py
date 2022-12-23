def f(g):
    if g <= 0:
        return 10**30
    return A/g**0.5 + B*(g-1)

A,B = map(int,input().split())

low = 0
high = 10**18

cnt = 500
while cnt:
    cnt -= 1
    c1 = (low*2 + high)/3
    c2 = (low + high*2)/3

    if f(c1) > f(c2):
        low = c1
    else:
        high = c2

ans = 10**30
for i in range(int(low)-3,int(low)+3):
    ans = min(ans,f(i))
for i in range(int(high)-3,int(high)+3):
    ans = min(ans,f(i))

print(ans)
