import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

a,b,c,d,e,f = map(int,input().split())
g,h,i,j,k,l = map(int,input().split())

if min(d,j) > max(a,g) and min(e,k) > max(b,h) and min(f,l) > max(c,i):
    print("Yes")
else:
    print("No")
