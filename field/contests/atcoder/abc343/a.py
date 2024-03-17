import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

A,B =  map(int,input().split())

for n in range(10):
    if n != A+B:
        print(n)
        exit()
