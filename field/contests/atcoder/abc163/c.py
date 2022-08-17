N = int(input())
A = list(map(int,input().split()))

cnt = [0]*(N+1)
for i in range(N-1):
    cnt[A[i]] += 1

for i in range(1,N+1):
    print(cnt[i])