import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

H = int(input())

h = 0
cnt = 0
while 1:
    h += 2**cnt
    if h > H:
        print(cnt+1)
        exit()
    cnt += 1
