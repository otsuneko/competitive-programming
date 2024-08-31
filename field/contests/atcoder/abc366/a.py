import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,T,A = map(int,input().split())
if T > N//2 or A > N//2:
    print("Yes")
else:
    print("No")
