import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())


# y軸を絞る
mi,ma = 1,N
rook = N
while (ma-mi > 0):
    mid = (mi+ma)//2
    print("?",mi,mid,1,N,flush=True)
    T = int(input())
    if mid-mi+1 == T:
        mi = mid+1
    else:
        ma = mid
y = mi

# x軸を絞る
mi,ma = 1,N
rook = N
while (ma-mi > 0):
    mid = (mi+ma)//2
    print("?",1,N,mi,mid,flush=True)
    T = int(input())
    if mid-mi+1 == T:
        mi = mid+1
    else:
        ma = mid
x = mi

print("!",y,x)