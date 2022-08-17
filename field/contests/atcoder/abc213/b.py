N = int(input())
A = list(map(int,input().split()))
A2 = []
for i in range(N):
    A2.append((A[i],i+1))

A2.sort()
print(A2[-2][1])