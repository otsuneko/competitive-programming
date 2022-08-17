X,N = map(int,input().split())
P = set(list(map(int,input().split())))
not_P = [i for i in range(102) if i not in P]

min_diff = 10**18
ans = 0
for np in not_P:
    if abs(np-X) < min_diff:
        ans = np
        min_diff = abs(np-X)

print(ans)
