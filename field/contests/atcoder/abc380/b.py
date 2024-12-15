import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = input()
A = []

S = S[1:]

cnt = 0
for i in range(len(S)):
    if S[i] == "-":
        cnt += 1
    else:
        A.append(cnt)
        cnt = 0
print(*A)
