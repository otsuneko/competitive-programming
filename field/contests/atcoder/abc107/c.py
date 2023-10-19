N,K = map(int,input().split())
X = list(map(int,input().split()))

ans = 10**18

if K == 1:
    for i in range(K):
        ans = min(ans,abs(X[i]))
elif K == N:
    ans = X[-1]-X[0] + min(abs(X[-1]),abs(X[0]))

for i in range(N-K):
    ans = min(ans, abs(X[i]) + X[i+K-1]-X[i])

X.sort(reverse=True)
for i in range(N):
    X[i] = -X[i]

for i in range(N-K):
    ans = min(ans, abs(X[i]) + X[i+K-1]-X[i])

print(ans)