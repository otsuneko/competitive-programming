N,K = map(int,input().split())
C = list(map(int,input().split()))
P = list(map(int,input().split()))

shirts = []
for c,p in zip(C,P):
    shirts.append([p,c])
shirts.sort()

ans = 0
check = set()
for shirt in shirts:
    if shirt[1] not in check:
        check.add(shirt[1])
        ans += shirt[0]
    if len(check) == K:
        print(ans)
        break
else:
    print(-1)