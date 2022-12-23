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

ans = 0
p = prime_decomposition(N)
while 2**ans < len(p):
    ans += 1
print(ans)


# def divisor(n):
#     lower_divisors , upper_divisors = [], []
#     i = 1
#     while i*i <= n:
#         if n % i == 0:
#             lower_divisors.append(i)
#             if i != n // i:
#                 upper_divisors.append(n//i)
#         i += 1
#     return lower_divisors + upper_divisors[::-1]

# import sys
# sys.setrecursionlimit(10**7)
# def dfs(n):
#     div = divisor(n)
#     a,b = div[len(div)//2-1], div[len(div)//2]

#     if len(div)%2:
#         return dfs(b) + 1
#     elif a > 1 and b > 1:
#         return max(dfs(a), dfs(b)) + 1
#     else:
#         return 0

# N = int(input())

# ans = dfs(N)
# print(ans)