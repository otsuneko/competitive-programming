def is_prime(n):
    for i in range(2, n + 1):
        if i * i > n:
            break
        if n % i == 0:
            return False
    return n != 1

X = int(input())
for i in range(X,10**5+4):
    if is_prime(i):
        print(i)
        break