import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18


A,B,C,D,E = map(int,input().split())
score = dict()
score['A'] = A
score['B'] = B
score['C'] = C
score['D'] = D
score['E'] = E

import itertools

ans = []
for cmb in itertools.combinations("ABCDE",1):
    result = 0
    for c in cmb:
        result += score[c]
    ans.append((result,"".join(list(cmb))))

for cmb in itertools.combinations("ABCDE",2):
    result = 0
    for c in cmb:
        result += score[c]
    ans.append((result,"".join(list(cmb))))

for cmb in itertools.combinations("ABCDE",3):
    result = 0
    for c in cmb:
        result += score[c]
    ans.append((result,"".join(list(cmb))))

for cmb in itertools.combinations("ABCDE",4):
    result = 0
    for c in cmb:
        result += score[c]
    ans.append((result,"".join(list(cmb))))

for cmb in itertools.combinations("ABCDE",5):
    result = 0
    for c in cmb:
        result += score[c]
    ans.append((result,"".join(list(cmb))))

ans.sort(key = lambda x: (-x[0],x[1]))


for r,name in ans:
    print(name)
