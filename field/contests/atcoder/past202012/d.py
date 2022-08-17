from operator import itemgetter
N = int(input())
S = []
for i in range(N):
    s = input()
    S.append([int(s), -len(s), s])

S.sort(key=itemgetter(0,1))
for s in S:
    print(s[2])