import itertools
N = int(input())
C = ["a","b","c"]

ans = itertools.product(C, repeat=N)

for a in ans:
    print("".join(a))