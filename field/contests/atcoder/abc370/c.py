import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = list(input())
T = list(input())
X = []

priority = []
for i in range(len(S)):
    priority.append(((ord(S[i])-ord(T[i]))*(26**(len(S)-i)), i))
priority.sort(reverse=True)

for p,i in priority:
    if S[i] != T[i]:
        S[i] = T[i]
        X.append("".join(S))

print(len(X))
for x in X:
    print("".join(x))
