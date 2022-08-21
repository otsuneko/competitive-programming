import itertools
import operator

N,P,Q,R = map(int,input().split())
A = list(map(int,input().split()))
cumsum = [0] + list(itertools.accumulate(A, func=operator.add))
check = set(cumsum)

for x in range(N-2):
    if cumsum[x]+P in check and cumsum[x]+P+Q in check and cumsum[x]+P+Q+R in check:
        print("Yes")
        exit()

print("No")