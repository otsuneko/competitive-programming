import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

masu = []
for i in range(3):
    tmp = list(map(int,input().split()))
    masu += tmp

import itertools

total = 0
success = 0
for ptr in itertools.permutations(range(9)):
    total += 1

    r1 = []
    r2 = []
    r3 = []
    c1 = []
    c2 = []
    c3 = []
    s1 = []
    s2 = []

    for p in ptr:
        if p in {0,1,2}:
            if len(r1) == 2 and len(set(r1)) == 1 and masu[p] != r1[0]:
                break
            r1.append(masu[p])
        if p in {3,4,5}:
            if len(r2) == 2 and len(set(r2)) == 1 and masu[p] != r2[0]:
                break
            r2.append(masu[p])
        if p in {6,7,8}:
            if len(r3) == 2 and len(set(r3)) == 1 and masu[p] != r3[0]:
                break
            r3.append(masu[p])
        if p in {0,3,6}:
            if len(c1) == 2 and len(set(c1)) == 1 and masu[p] != c1[0]:
                break
            c1.append(masu[p])
        if p in {1,4,7}:
            if len(c2) == 2 and len(set(c2)) == 1 and masu[p] != c2[0]:
                break
            c2.append(masu[p])
        if p in {2,5,8}:
            if len(c3) == 2 and len(set(c3)) == 1 and masu[p] != c3[0]:
                break
            c3.append(masu[p])
        if p in {0,4,8}:
            if len(s1) == 2 and len(set(s1)) == 1 and masu[p] != s1[0]:
                break
            s1.append(masu[p])
        if p in {2,4,6}:
            if len(s2) == 2 and len(set(s2)) == 1 and masu[p] != s2[0]:
                break
            s2.append(masu[p])
    else:
        success += 1

print(success/total)