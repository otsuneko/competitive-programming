P = int(input())
import math

for i in range(1,12):
    if P <= math.factorial(i):
        break

ans = 0
i -= 1
while P > 0:
    n = P//math.factorial(i)
    P -= n*math.factorial(i)
    ans += n
    i -= 1
print(ans)