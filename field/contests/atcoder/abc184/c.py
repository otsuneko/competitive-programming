r1,c1 = map(int,input().split())
r2,c2 = map(int,input().split())

# 0手
if r1 == r2 and c1 == c2:
    print(0)
# 1手
elif r1+c1 == r2+c2 or r1-c1 == r2-c2 or abs(r1-r2) + abs(c1-c2) <= 3:
    print(1)
# 2手
elif abs(r1-r2) + abs(c1-c2) <= 6 or -3 <= abs((r1+c1) - (r2+c2)) <= 3 or -3 <= abs((r1-c1) - (r2-c2)) <= 3 or ((r1+c1) - (r2+c2))%2 == 0 or ((r1-c1) - (r2-c2))%2 == 0:
    print(2)
# 3手
else:
    print(3)