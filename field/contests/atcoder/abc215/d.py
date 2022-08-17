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

N,M = map(int,input().split())
A = list(map(int,input().split()))

primes = set()
for a in A:
    s = set(prime_decomposition(a))
    primes |= s

check = [True]*(M+1)

for p in primes:
    for i in range(p, M+1, p):
        check[i] = False

print(check[1:].count(True))
for i in range(1,M+1):
    if check[i]:
        print(i)