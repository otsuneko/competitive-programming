A,B = map(int,input().split())
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

print(Decimal(str(B/A)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
#123.46