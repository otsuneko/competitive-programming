import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
ta, ao = 0,0
for _ in range(N):
    x,y = map(int,input().split())
    ta, ao = ta+x, ao+y

if ta > ao:
    print("Takahashi")
elif ta < ao:
    print("Aoki")
else:
    print("Draw")