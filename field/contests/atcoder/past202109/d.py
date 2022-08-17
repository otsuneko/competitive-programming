def divisor(n):
    lower_divisors , upper_divisors = [], []
    i = 1
    while i*i <= n:
        if n % i == 0:
            lower_divisors.append(i)
            if i != n // i:
                upper_divisors.append(n//i)
        i += 1
    return lower_divisors + upper_divisors[::-1]

X,Y = map(int,input().split())
num_X = len(divisor(X))
num_Y = len(divisor(Y))

if num_X > num_Y:
    print("X")
elif num_Y > num_X:
    print("Y")
else:
    print("Z")