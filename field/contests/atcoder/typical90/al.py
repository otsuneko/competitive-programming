def gcd(a,b):
    if b == 0:
        return a
    else:
        return gcd(b,a%b)

def lcm(a, b):
    return a * b // gcd (a, b)

A,B = map(int,input().split())
if A < B:
    A,B = B,A

# if A == 10**18:
#     if B == 1:
#         print(10**18)
#     else:
#         print("Large")
# else:
#     n = lcm(A,B)
#     if n > 10**18:
#         print("Large")
#     else:
#         print(n)
n = lcm(A,B)
if n > 10**18:
    print("Large")
else:
    print(n)