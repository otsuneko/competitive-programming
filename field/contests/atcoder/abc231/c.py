import bisect
'''
bisect.bisect(A,x) #ソートされたリストAにソートを崩さずに値xを挿入するとき、xの入るべきインデックスを返す。
bisect.bisect_left(A,x) #リストAに値xを入れ、xが複数になるとき、一番左の値xのインデックスを返す
bisect.bisect_right(A,x) #リストAに値xを入れ、xが複数になるとき、一番右の値xのインデックスを返す(bisect.bisectと同じ)
'''
N,Q = map(int,input().split())
A = list(map(int,input().split()))
A.sort()
for _ in range(Q):
    x = int(input())
    print(N-bisect.bisect_left(A,x))