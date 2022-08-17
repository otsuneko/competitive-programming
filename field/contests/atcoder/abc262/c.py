N = int(input())
A = list(map(int,input().split()))

same = [0]*N
for i in range(N):
    if A[i] == i+1:
        same[i] = 1

cumsum = [0]*(N+1)
for i in range(N-1,-1,-1):
    cumsum[i] = cumsum[i+1] + same[i]
# print(same)
# print(cumsum)

ans = 0
for i in range(N):
    if same[i]:
        ans += cumsum[i+1]
    else:
        if A[A[i]-1] == i+1 and A[i] < A[A[i]-1]:
            ans += 1
    # print(ans)
print(ans)