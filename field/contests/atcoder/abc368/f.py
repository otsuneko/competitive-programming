import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

def prime_decomposition(n):
    i = 2
    table = []
    while i * i <= n:
        while n % i == 0:
            n = n//i
            table.append(i)
        i += 1
    if n > 1:
        table.append(n)
    return table

N = int(input())
A = list(map(int,input().split()))

li = []
for a in A:
    primes = prime_decomposition(a)
    li.append(len(primes))

grundy = 0
for n in li:
    grundy ^= n
if grundy == 0:
    print("Bruno")
else:
    print("Anna")
