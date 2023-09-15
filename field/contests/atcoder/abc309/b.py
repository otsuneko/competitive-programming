import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
A = [list(input()) for _ in range(N)]
inv = list(zip(*A))

li = A[0]
li2 = list(inv[N-1])
li3 = A[N-1]
li4 = list(inv[0])

# print(li,li2,li3,li4)

ans = [li4[1]] + li[:N-1]
print("".join(ans))

for i in range(1,N-1):
    ans = [li4[i+1]] + A[i][1:N-1] + [li2[i-1]]
    print("".join(ans))

ans = li3[1:N] + [li2[N-2]]
print("".join(ans))
