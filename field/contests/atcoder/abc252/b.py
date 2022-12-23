N,K = map(int,input().split())
A = list(map(int,input().split()))
B = list(map(int,input().split()))

ma = max(A)
for i in range(N):
    if A[i] == ma:
        if i+1 in B:
            print("Yes")
            exit()
print("No")