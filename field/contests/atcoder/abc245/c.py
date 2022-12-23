N,K =map(int,input().split())
A =list(map(int,input().split()))
B =list(map(int,input().split()))

X = []
for i in range(N):
    X.append(sorted([A[i],B[i]]))

ans = "Yes"

cand = [X[0][0],X[0][1]]
for i in range(N-1):
    nxt = set()
    for c in cand:
        for x in X[i+1]:
            if abs(c-x) <= K:
                nxt.add(x)
    if len(nxt) == 0:
        ans = "No"
        break
    cand = nxt
# print(cand)
print(ans)