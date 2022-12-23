N = int(input())

for h in range(1,3501):
    for n in range(1,3501):
        if h+n == (4*h*n)/N:
            continue
        if h*n%((4*h*n)/N-h-n)==0 and 0 < h*n/((4*h*n)/N-h-n):
            print(h,n,int(h*n/((4*h*n)/N-h-n)))
            exit()
