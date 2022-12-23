n = int(input())
A = [0]*n
B = [0]*n
for i in range(n):
    A[i],B[i]=map(int,input().split())
A.sort()
B.sort()

def median(li):
    if n%2==1:
        return li[n//2]
    else:
        return sum(li[n//2-1:n//2+1])
print(median(B)-median(A)+1)