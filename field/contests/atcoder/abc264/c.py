H1,W1 = map(int,input().split())
A = [list(map(int,input().split())) for _ in range(H1)]
H2,W2 = map(int,input().split())
B = [list(map(int,input().split())) for _ in range(H2)]

import itertools
for bitH in itertools.product([True, False], repeat=H1):
    for bitW in itertools.product([True, False], repeat=W1):
        grid = []
        for i,b1 in enumerate(bitH):
            if not b1:
                continue
            tmp = []
            for j,b2 in enumerate(bitW):
                if b2:
                    tmp.append(A[i][j])
            grid.append(tmp)
        if grid == B:
            print("Yes")
            exit()
print("No")