import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
S = input()

s = set()
for i in range(N):
    s.add(S[i])
    if len(s) == 3:
        print(i+1)
        exit()