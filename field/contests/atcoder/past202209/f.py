N = int(input())
A = list(map(int,input().split()))

X = []
for _ in range(N):
    C = int(input())
    X.append(set(list(map(int,input().split()))))

M = 10**5+1
allergen = [set() for _ in range(M)]
total = set()
for i,x in enumerate(X):
    for a in x:
        allergen[a-1].add((A[i],i))
        total.add((A[i],i))

Q = int(input())
for _ in range(Q):
    D = int(input())
    Y = set(list(map(int,input().split())))

    ng = set()
    for y in Y:
        ng |= allergen[y-1]

    ok = total - ng
    # print(ok)
    if not ok:
        print(-1)
        continue

    max_i, max = -1,0
    for x,i in ok:
        if x > max:
            max = x
            max_i = i
    print(max_i+1)