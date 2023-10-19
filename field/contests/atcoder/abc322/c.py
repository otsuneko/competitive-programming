import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
'''
bisect(A,x) #ソートされたリストAにソートを崩さずに値xを挿入するとき、xの入るべきインデックスを返す。
bisect_left(A,x) #リストAに値xを入れ、xが複数になるとき、一番左の値xのインデックスを返す。
bisect_right(A,x) #リストAに値xを入れ、xが複数になるとき、一番右の値xのインデックスを返す(bisect.bisectと同じ)。
insort(A,x) #リストAに含まれるxのうち、どのエントリーよりも後ろにxをO(N)で挿入する。
'''

N,M = map(int,input().split())
A = list(map(int,input().split()))
B = [0]

idx = 0
for day in range(1,N+1):
    if day == A[idx]:
        B.append(B[-1]+1)
        idx += 1
    else:
        B.append(B[-1])

# print(B)
hanabi = 0
for day in range(1,N):
    idx = bisect(B,hanabi)
    # print(idx)
    if idx == day:
        hanabi+=1
    print(idx-day)
print(0)