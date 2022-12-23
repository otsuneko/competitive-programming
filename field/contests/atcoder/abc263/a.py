X = list(map(int,input().split()))
from collections import Counter
count = Counter(X)
s = list(set(X))

if len(s) == 2 and ([count[s[0]],count[s[1]]] == [3,2] or [count[s[0]],count[s[1]]] == [2,3]):
    print("Yes")
else:
    print("No")