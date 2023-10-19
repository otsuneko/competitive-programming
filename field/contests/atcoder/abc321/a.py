import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = input()

cur = int(N[0])
for i in range(1,len(N)):
    if int(N[i]) >= cur:
        print("No")
        exit()
    cur = int(N[i])
print("Yes")