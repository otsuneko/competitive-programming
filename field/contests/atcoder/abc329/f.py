import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,Q = map(int,input().split())
C = list(map(int,input().split()))

s = [set() for _ in range(N)]
for i in range(N):
    s[i].add(C[i])

for _ in range(Q):
    a,b = map(int,input().split())
    a,b = a-1,b-1

    if len(s[a]) > len(s[b]):
        s[a],s[b] = s[b],s[a]
    s[b] |= s[a]
    s[a] = set()
    print(len(s[b]))