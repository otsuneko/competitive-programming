from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
'''
bisect(A,x) #ソートされたリストAにソートを崩さずに値xを挿入するとき、xの入るべきインデックスを返す。
bisect_left(A,x) #リストAに値xを入れ、xが複数になるとき、一番左の値xのインデックスを返す。
bisect_right(A,x) #リストAに値xを入れ、xが複数になるとき、一番右の値xのインデックスを返す(bisect.bisectと同じ)。
insort(A,x) #リストAに含まれるxのうち、どのエントリーよりも後ろにxをO(N)で挿入する。
'''
N,K = map(int,input().split())
A = list(map(int,input().split()))
A2 = sorted(A)

li = []
for k in range(K):
    tmp = []
    idx = k
    while idx < N:
        insort(tmp,A[idx])
        idx += K
    li.append(tmp)

A3 = []
idx = 0
for i in range(-(-(N)//K)):
    for l in li:
        if i < len(l):
            A3.append(l[i])

if A3 == A2:
    print("Yes")
else:
    print("No")