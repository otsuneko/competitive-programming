N,x = map(int,input().split())
A = list(map(int,input().split()))
A.sort()
su = sum(A)

if su == x:
    print(N)
elif su < x:
    print(N-1)
else:
    ans = 0
    for a in A:
        if x >= a:
            x -= a
            ans += 1
        else:
            break
    print(ans)