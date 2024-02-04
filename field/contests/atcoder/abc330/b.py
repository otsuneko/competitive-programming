import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,S,M,L = map(int,input().split())

ans = INF
for s in range(N//6+5):
    for m in range(N//8+5):
        for l in range(N//12+5):
            if 6*s+8*m+12*l >= N:
                ans = min(ans,s*S+m*M+l*L)
print(ans)