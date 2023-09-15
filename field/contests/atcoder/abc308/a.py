import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

S = list(map(int,input().split()))

ma = -1
for s in S:
    if s < ma:
        print("No")
        exit()
    if not (100 <= s <= 675):
        print("No")
        exit()
    if not s%25 == 0:
        print("No")
        exit()
    ma = s
print("Yes")