import itertools
N,K =map(int,input().split())
A =list(map(int,input().split()))

ans = 10**18
cmb = list(itertools.combinations([i for i in range(N)],K))
for c in cmb:

    cost = 0
    h = A[0]
    for i in range(1,N):
        if i in c:
            if A[i] > h:
                h = A[i]
            else:
                cost += h - A[i] + 1
                h += 1
        else:
            h = max(h, A[i])


    ans = min(ans, cost)

print(ans)