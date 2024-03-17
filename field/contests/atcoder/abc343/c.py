import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N =  int(input())

ans = 0
for i in range(10**6+1):
    x = str(i**3)
    if int(x) > N:
       break
    if x == x[::-1]:
        ans = max(ans,int(x))

print(ans)
