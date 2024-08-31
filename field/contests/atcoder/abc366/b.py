import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
S = [input() for _ in range(N)]

S2 = []
for s in S:
    S2.append(s + "*"*100)

S3 = list(zip(*S2[::-1]))

for s in S3:
    flg = False
    for i in range(len(s)):
        if s[i] != "*":
            flg = True
            break
    if flg:
        print("".join(s).rstrip("*"))
    else:
        break
