N = int(input())
A = list(map(int,input().split()))
B = list(map(int,input().split()))

ans = set([])
for i in range(N):
    x = A[0]^B[i]
    check = set([])
    for j in range(N):
        check.add(x^B[j])
    if check == set(A):
        ans.add(x)

ans = list(ans)
ans.sort()
print(len(ans))
for a in ans:
    print(a)