import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

colors = ["Red", "Green", "Blue"]

prices = list(map(int,input().split()))
C = input()

idx = colors.index(C)
prices[colors.index(C)] = INF
print(min(prices))
