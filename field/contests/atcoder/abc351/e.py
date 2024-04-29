import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
points = [list(map(int, input().split())) for _ in range(N)]

# 座標を45度回転し、X軸とY軸で独立に考える
X_odd = []
Y_odd = []
X_even = []
Y_even = []
for x,y in points:
    if (x+y)%2 == 0:
        X_even.append(x-y)
        Y_even.append(x+y)
    else:
        X_odd.append(x-y)
        Y_odd.append(x+y)
X_odd.sort()
Y_odd.sort()
X_even.sort()
Y_even.sort()

import itertools
import operator
cumsumX_odd = [0] + list(itertools.accumulate(X_odd, func=operator.add))
cumsumY_odd = [0] + list(itertools.accumulate(Y_odd, func=operator.add))
cumsumX_even = [0] + list(itertools.accumulate(X_even, func=operator.add))
cumsumY_even = [0] + list(itertools.accumulate(Y_even, func=operator.add))

ans = 0
for i,x in enumerate(X_odd):
    su = cumsumX_odd[-1] - cumsumX_odd[i+1]
    ans += su - x*(len(X_odd)-1-i)

for i,y in enumerate(Y_odd):
    su = cumsumY_odd[-1] - cumsumY_odd[i+1]
    ans += su - y*(len(Y_odd)-1-i)

for i,x in enumerate(X_even):
    su = cumsumX_even[-1] - cumsumX_even[i+1]
    ans += su - x*(len(X_even)-1-i)

for i,y in enumerate(Y_even):
    su = cumsumY_even[-1] - cumsumY_even[i+1]
    ans += su - y*(len(Y_even)-1-i)

print(ans//2)
