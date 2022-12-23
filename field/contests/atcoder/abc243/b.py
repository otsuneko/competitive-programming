N =int(input())
A =list(map(int,input().split()))
B =list(map(int,input().split()))

ans1 = 0
for i in range(N):
    if A[i] == B[i]:
        ans1 += 1

print(ans1)
print(len(set(A)&set(B))-ans1)