from collections import Counter
N =int(input())
A =list(map(int,input().split()))

count = Counter(A)

for key in count:
    if count[key] == 3:
        print(key)
        break
