# def xor(n):
#     if n%2:
#         return (n+1)//2%2
#     else:
#         return ((n+2)//2%2) ^ (n+1)

# Direct XOR of all numbers from 1 to n
def allXOR(n):
    if n%4 == 0:
        return n
    elif n%4 == 1:
        return 1
    elif n%4 == 2:
        return n+1
    elif n%4 == 3:
        return 0

A,B = map(int,input().split())
fa = allXOR(A-1)
fb = allXOR(B)

print(fa^fb)