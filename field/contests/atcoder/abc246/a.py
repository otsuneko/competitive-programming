X = []
Y = []
for _ in range(3):
    x,y =map(int,input().split())
    X.append(x)
    Y.append(y)

ans = [0,0]
for x in X:
    if X.count(x) == 1:
        ans[0] = x

for y in Y:
    if Y.count(y) == 1:
        ans[1] = y

print(*ans)