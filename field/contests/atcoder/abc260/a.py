from collections import Counter
S = input()
count = Counter(S)

for c in count:
    if count[c] == 1:
        print(c)
        exit()
print(-1)