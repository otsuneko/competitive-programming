import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())

yes = set()
for i in range(2, 10**5+1):
    for j in range(2, 100):
        if i**j <= N:
            yes.add(i**j)
        else:
            break
print(N-len(yes))
