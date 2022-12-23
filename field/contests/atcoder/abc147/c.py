N = int(input())
evidence = []
for _ in range(N):
    A = int(input())
    tmp = []
    for _ in range(A):
        x,y = map(int,input().split())
        tmp.append((x-1,y))
    evidence.append(tmp)
# print(evidence)

import itertools

ans = 0
for bit in itertools.product([True, False], repeat=N):
    for i,person in enumerate(evidence):
        iskind = bit[i]
        for say in person:
            if iskind:
                if (say[1] == 1 and bit[say[0]] == False) or (say[1] == 0 and bit[say[0]] == True):
                    break
            else:
                continue
        else:
            continue
        break
    else:
        ans = max(ans,bit.count(True))
print(ans)