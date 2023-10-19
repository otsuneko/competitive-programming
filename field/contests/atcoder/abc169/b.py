N = int(input())
A = list(map(int,input().split()))
A.sort()

ans = 1
for a in A:
    if ans * a > 10**18:
        print(-1)
        exit()
    ans *= a
print(ans)