A,B,C,D,E,F,X =map(int,input().split())

tak = ao = 0

cur = X
while cur > 0:
    if cur >= A:
        cur -= A
        tak += A*B
    elif cur > 0:
        tak += cur*B
        cur = 0
    
    if cur >= C:
        cur -= C
    else:
        break

cur = X
while cur > 0:
    if cur >= D:
        cur -= D
        ao += D*E
    elif cur > 0:
        ao += cur*E 
        cur = 0

    if cur >= F:
        cur -= F
    else:
        break

if tak > ao:
    print("Takahashi")
elif tak == ao:
    print("Draw")
else:
    print("Aoki")