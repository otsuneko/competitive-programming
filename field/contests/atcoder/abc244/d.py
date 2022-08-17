S = list(map(str,input().split()))
T = list(map(str,input().split()))

from collections import defaultdict
dict = defaultdict(int)

for i in range(3):
    dict[S[i]] = i
    S[i] = i
for i in range(3):
    T[i] = dict[T[i]]

if T in [[0,2,1],[1,0,2],[2,1,0]]:
    print("No")
else:
    print("Yes")