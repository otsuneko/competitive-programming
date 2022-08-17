import itertools

S = list(input())
ptr = set(list(itertools.permutations(S)))
print(len(ptr))