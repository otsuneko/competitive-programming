N,K = map(int,input().split())
A = list(map(int,input().split()))
B = list(map(int,input().split()))

diff_sum = 0
for a,b in zip(A,B):
    diff_sum += abs(a-b)

if K >= diff_sum and (K-diff_sum)%2 == 0:
    print("Yes")
else:
    print("No")