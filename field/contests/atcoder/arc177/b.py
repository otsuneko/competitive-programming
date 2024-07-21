import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
S = list(input())

ans = []
for i in range(N-1,-1,-1):
    if S[i] == "1":
        ans += ["A"]*(i+1)
        ans += ["B"]*i
    else:
        continue
print(len(ans))
print("".join(ans))
