N = int(input())
S = [list(input()) for _ in range(N)]

for s in S[::-1]:
    print("".join(s))