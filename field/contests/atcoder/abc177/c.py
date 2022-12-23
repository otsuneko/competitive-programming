import itertools
import operator
N = int(input())
A = list(map(int,input().split()))

cumsum = [0] + list(itertools.accumulate(A, func=operator.add))

ans = 0
for i in range(N-1):
    ans = (ans + A[i] * (cumsum[N]-cumsum[i+1]))%(10**9+7)

print(ans)