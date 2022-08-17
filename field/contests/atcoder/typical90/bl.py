N,Q = map(int,input().split())
A = list(map(int,input().split()))
diff = []
ans = 0
for i in range(N-1):
    diff.append(A[i+1]-A[i])
    ans += abs(A[i+1]-A[i])

for _ in range(Q):
    L,R,V = map(int,input().split())
    L,R = L-1,R-1

    if L-1 >= 0:
        ans -= abs(diff[L-1])
        diff[L-1] = diff[L-1] + V
    if R < N-1:
        ans -= abs(diff[R])
        diff[R] = diff[R] - V

    if L-1 >= 0:
        ans += abs(diff[L-1])
    if R < N-1:
        ans += abs(diff[R])
    print(ans)