import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())

bin_x = bin(N)[2:]

ans = 0
for i in range(len(bin_x)-1,-1,-1):
    if bin_x[i] == "0":
        ans += 1
    else:
        print(ans)
        exit()