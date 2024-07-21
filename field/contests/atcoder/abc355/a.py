import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

A,B = map(int,input().split())

if len(set([A,B])) == 1:
    print(-1)
else:
    print(list(set([1,2,3])-set([A,B]))[0])
