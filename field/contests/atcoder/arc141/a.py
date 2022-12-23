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

T = int(input())
for _ in range(T):
    N = int(input())
    div = divisor(len(str(N)))
    strN = str(N)

    ans = int("9"*(len(strN)-1))
    for d in reversed(div[1:]):
        # print(d)
        for i in range(int(strN[:div[-1]//d]),0,-1):
            n = int(str(i)*d)
            if n <= N:
                ans = max(ans,n)
                break
    print(ans)