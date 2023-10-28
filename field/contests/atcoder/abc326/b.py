import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())

for i in range(N,1000):
    n = str(i)
    if int(n[0])*int(n[1]) == int(n[2]):
        print(n)
        exit()