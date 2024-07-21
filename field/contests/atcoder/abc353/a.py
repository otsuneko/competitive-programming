import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
H = list(map(int,input().split()))

for i in range(1,N):
    if H[0] < H[i]:
        print(i+1)
        exit()
print(-1)
