import bisect
'''
bisect.bisect(A,x) #ソートされたリストAにソートを崩さずに値xを挿入するとき、xの入るべきインデックスを返す。
bisect.bisect_left(A,x) #リストAに値xを入れ、xが複数になるとき、一番左の値xのインデックスを返す
bisect.bisect_right(A,x) #リストAに値xを入れ、xが複数になるとき、一番右の値xのインデックスを返す(bisect.bisectと同じ)
'''

a = list(input())
b = list(input())

from collections import Counter
cnt_a = Counter(a)
cnt_b = Counter(b)
print(cnt_a)
print(cnt_b)

ans1 = []
ans2 = []
for key in cnt_a:
    if cnt_b[10-key] > 0:
        ans1.append(key)
        ans2.append(10-key)
        cnt_a[key] -= 1
        cnt_b[10-key] -= 1
    for key in cnt_a:
