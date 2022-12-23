N,M =map(int,input().split())
A =list(map(int,input().split()))
B =list(map(int,input().split()))

ans = True
for b in B:
    idx = -1
    if b in A:
        idx = A.index(b)
    if idx == -1:
        print("No")
        exit()
    else:
        A[idx] = -1

print("Yes")
