from collections import defaultdict

def prime_decomposition(n):
  i = 2
  dict = defaultdict(int)
  while i * i <= n:
    while n % i == 0:
      n = n//i
      dict[i] += 1
    i += 1
  if n > 1:
    dict[n] += 1
  return dict

N = int(input())

sqpw = []
for i in range(1,N+1):
    sqpw.append(i*i)

ans = 0
for i in range(1,N+1):
    if i == 1:
        primes = defaultdict(int)
        primes[1] = 1
    else:
        primes = prime_decomposition(i)
    
    mul = 1
    for key in primes:
        if primes[key]%2:
            mul *= key
    
    for p in sqpw:
        if mul*p > N:
            break
        ans += 1

print(ans)