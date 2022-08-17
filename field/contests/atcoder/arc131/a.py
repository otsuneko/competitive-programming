A=input()
B=input()

if int(B)%2:
    B2 = str(int(B)//2) + "5"
else:
    B2 = str(int(B)//2)

print(A + B2)