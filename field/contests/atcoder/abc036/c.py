def compress(arr):
    *XS, = set(arr)
    XS.sort()
    return {e: i for i, e in enumerate(XS)}

N =int(input())
A =[int(input()) for _ in range(N)]
B = compress(A)

for a in A:
    print(B[a])