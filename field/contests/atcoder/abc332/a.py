import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N,S,K =  map(int,input().split())
goods = [list(map(int,input().split())) for _ in range(N)]

ans = 0
for p,q in goods:
    money = p*q
    ans += money
if ans < S:
    ans += K

print(ans)