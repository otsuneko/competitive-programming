import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,M = map(int,input().split())
A = list(map(int,input().split()))
B = list(map(int,input().split()))
C = sorted(A+B)

s = set(A)
cnt = 0
for c in C:
    if cnt == 1 and c in s:
        print("Yes")
        exit()
    elif cnt == 0 and c in s:
        cnt += 1
    else:
        cnt = 0
print("No")
