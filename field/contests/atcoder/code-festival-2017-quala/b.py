N,M,K = map(int,input().split())

s = set([0,N*M])

for i in range(1,N):
    s.add(i*M)
    for j in range(1,M):
        before = i
        after = N-i
        diff = after-before
        s.add(i*M+diff*j)

for i in range(1,M):
    s.add(i*N)
    for j in range(1,N):
        before = i
        after = M-i
        diff = after-before
        s.add(i*N+diff*j)

print(["No","Yes"][K in s])