from decimal import Decimal
import math
a,b = input().split()
a = Decimal(a)
b = Decimal(b)
print(math.floor(a*b))
