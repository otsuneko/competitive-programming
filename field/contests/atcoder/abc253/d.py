def gcd(a,b):
    if b == 0:
        return a
    else:
        return gcd(b,a%b)

def lcm(a, b):
    return a * b // gcd (a, b)

N,A,B = map(int,input().split())

AB = lcm(A,B)

s = (1+N)*N//2
max_A = N//A*A
sA = (A+max_A)*(max_A//A)//2
max_B = N//B*B
sB = (B+max_B)*(max_B//B)//2
max_AB = N//AB*AB
sAB = (AB+max_AB)*(max_AB//AB)//2

print(s-sA-sB+sAB)