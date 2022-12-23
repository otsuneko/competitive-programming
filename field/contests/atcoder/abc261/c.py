from collections import defaultdict
dict = defaultdict(int)

N = int(input())
for _ in range(N):
    S = input()
    if dict[S] == 0:
        print(S)
    else:
        print(S + "(" + str(dict[S]) + ")" )

    dict[S] += 1
