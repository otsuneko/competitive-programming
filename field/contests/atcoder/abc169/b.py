n = int(input())
A = sorted(list(map(int,input().split())))
mod = 10**18

a = A.pop(0)
for i in range(len(A)):
    a=a*A[i]
    if a>mod:
        print(-1)
        exit()
print(a)