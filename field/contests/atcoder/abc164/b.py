A,B,C,D = map(int,input().split())

while 1:
    C -= B
    if C <= 0:
        print("Yes")
        break
    A -= D
    if A <= 0:
        print("No")
        break