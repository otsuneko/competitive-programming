N,M = map(int,input().split())
S = [list(input()) for _ in range(N)]

import itertools

for ptr in itertools.permutations(S):
    for i in range(N-1):
        diff = 0
        for j in range(M):
            if ptr[i][j] != ptr[i+1][j]:
                diff += 1
        if diff != 1:
            break
    else:
        print("Yes")
        exit()
print("No")