import numpy

N,M = map(int,input().split())
A =numpy.array(list(map(int,input().split()))[::-1])
C = numpy.array(list(map(int,input().split()))[::-1])

qx,rx = numpy.polynomial.polynomial.polydiv(C,A)
ans = list(map(int, qx))[::-1]
print(*ans)
