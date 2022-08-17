N = int(input())
A = list(map(int,input().split()))

A.sort()

for i in range(N):
    if i+1 != A[i]:
        print("No")
        exit()
else:
    print("Yes")