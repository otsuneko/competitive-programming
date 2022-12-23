from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
'''
bisect(A,x) #ソートされたリストAにソートを崩さずに値xを挿入するとき、xの入るべきインデックスを返す。
bisect_left(A,x) #リストAに値xを入れ、xが複数になるとき、一番左の値xのインデックスを返す。
bisect_right(A,x) #リストAに値xを入れ、xが複数になるとき、一番右の値xのインデックスを返す(bisect.bisectと同じ)。
insort(A,x) #リストAに含まれるxのうち、どのエントリーよりも後ろにxをO(N)で挿入する。
'''
N =int(input())
A =list(map(int,input().split()))
B =list(map(int,input().split()))
C =list(map(int,input().split()))
A.sort()
B.sort()
C.sort()

ans = 0
for b in B:
    aidx = bisect(A,b-1)

    cidx = bisect(C,b)

    ans += aidx * (N-cidx)
    # print(ans)

print(ans)