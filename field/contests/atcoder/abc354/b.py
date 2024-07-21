import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
users = []
T = 0
for _ in range(N):
    s,c = map(str, input().split())
    users.append(s)
    T += int(c)
users.sort()
print(users[T%N])
