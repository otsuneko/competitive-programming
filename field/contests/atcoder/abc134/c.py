N = int(input())
ma,ma2 = 0,0
A = []
for _ in range(N):
    a = int(input())
    A.append(a)
    if a > ma:
        ma2 = ma
        ma = a
    elif a > ma2:
        ma2 = a

for a in A:
    if a == ma:
        print(ma2)
    else:
        print(ma)