from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
'''
bisect(A,x) #ソートされたリストAにソートを崩さずに値xを挿入するとき、xの入るべきインデックスを返す。
bisect_left(A,x) #リストAに値xを入れ、xが複数になるとき、一番左の値xのインデックスを返す。
bisect_right(A,x) #リストAに値xを入れ、xが複数になるとき、一番右の値xのインデックスを返す(bisect.bisectと同じ)。
insort(A,x) #リストAに含まれるxのうち、どのエントリーよりも後ろにxをO(N)で挿入する。
'''

N =int(input())
S = input()

from collections import defaultdict
dict = defaultdict(list)

for i,c in enumerate(S):
    dict[int(c)].append(i)

ans = 0
for i in range(10):
    for j in range(10):
        for k in range(10):
            if len(dict[i]) == 0:
                continue
            idx1 = dict[i][0]
            tmp = bisect(dict[j],idx1)
            if tmp == len(dict[j]):
                continue
            idx2 = dict[j][tmp]
            tmp = bisect(dict[k],idx2)
            if tmp == len(dict[k]):
                continue
            idx3 = dict[k][tmp]
            # print(i,j,k,idx1,idx2,idx3,len(dict[k]),dict[k])
            ans += 1

print(ans)

