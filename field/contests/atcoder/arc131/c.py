N = int(input())
A = list(map(int,input().split()))
check = set(A)
used = set()
xor = 0
t = -1
flg = False
for i in range(N):
    xor ^= A[i]
    used.add(A[i])
    if xor in check and xor not in used:
        flg = True
        t = i

if (flg and t%2) or N == 1:
    print("Win")
else:
    print("Lose")