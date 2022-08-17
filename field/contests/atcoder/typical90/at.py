from collections import Counter
N = int(input())
A = list(map(int,input().split()))
B = list(map(int,input().split()))
C = list(map(int,input().split()))

for i in range(N):
    A[i] %= 46
    B[i] %= 46
    C[i] %= 46

cnt_A = Counter(A)
cnt_B = Counter(B)
cnt_C = Counter(C)

ans = 0
for i in range(47):
    for j in range(47):
        for k in range(47):
            if (i+j+k)%46 == 0:
                ans += cnt_A[i]*cnt_B[j]*cnt_C[k]

print(ans)