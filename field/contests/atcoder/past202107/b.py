A,B,C = map(int,input().split())

while 1:
    if A <= B*C:
        break
    A -= 1

print(A/B)