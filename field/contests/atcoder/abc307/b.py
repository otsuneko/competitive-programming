import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
S = [list(input()) for _ in range(N)]

for i in range(N):
    for j in range(N):
        if i == j:
            continue
        con = S[i] + S[j]
        if con == con[::-1]:
            print("Yes")
            exit()
print("No")