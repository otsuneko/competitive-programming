import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
bin_n = bin(N)[2:]

que = [0]
for i in range(len(bin_n)):
    tmp = que[:]
    if bin_n[i] == "0":
        continue
    for x in tmp:
        new = x + (2**(len(bin_n)-i-1))
        que.append(new)

que.sort()
for x in que:
    print(x)