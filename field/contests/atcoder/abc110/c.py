S = list(input())
T = list(input())

from collections import defaultdict
dict = defaultdict(set)

for s,t, in zip(S,T):
    if s != t:
        dict[t].add(s)
# print(dict)

for key in dict:
    if len(dict[key]) > 1:
        print("No")
        exit()
print("Yes")