import itertools
import itertools
import operator

N =int(input())
li = [i for i in range(N)]
if N == 1:
    print(0)
elif N%2:
    print(-1)
elif N%4 == 0:
    print(*li)
# else:

for ptr in itertools.permutations(li):
    cumsum = [0] + list(itertools.accumulate(ptr, func=operator.add))
    for i in range(len(cumsum)):
        cumsum[i] %= N
    if len(set(cumsum[1:])) == N:
        print(ptr,cumsum[1:])
