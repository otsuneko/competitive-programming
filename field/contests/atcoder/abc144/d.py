

import math
a,b,x =map(int,input().split())

h = x/a/a

if a*a*b/2 < x:
    ans = 90 - math.degrees(math.atan2(a/2,b-h))
else:
    c = 2*x/a/b
    ans = 90 - math.degrees(math.atan2(c,b))
print(ans)