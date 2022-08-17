def gcd(a,b):
    if b == 0:
        return a
    else:
        return gcd(b,a%b)

def lcm(a, b):
    return a * b // gcd (a, b)

def solve(limit):

    res = limit//C + limit//D - limit//LCM
    return res

A,B,C,D = map(int,input().split())
LCM = lcm(C,D)

ans = (B-A+1) - (solve(B)-solve(A-1))
print(ans)

### original code
# A,B,C,D = map(int,input().split())
# LCM = lcm(C,D)

# first_mul_C = (C+A-1)//C * C
# last_mul_C = B//C * C
# cnt_C = (last_mul_C-first_mul_C + C)//C

# first_mul_D = (D+A-1)//D * D
# last_mul_D = B//D * D
# cnt_D = (last_mul_D-first_mul_D+ D)//D

# first_mul_LCM = (LCM+A-1)//LCM * LCM
# last_mul_LCM = B//LCM * LCM
# cnt_LCM = (last_mul_LCM-first_mul_LCM+LCM)//LCM

# # print(cnt_C,cnt_D,cnt_LCM)
# print(B-A+1 - (cnt_C+cnt_D-cnt_LCM))