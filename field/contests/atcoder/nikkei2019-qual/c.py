N = int(input())
dish = []
for _ in range(N):
    a,b = map(int,input().split())
    dish.append((a+b,a,b))

dish.sort(reverse=True)

ta = 0
ao = 0
for i in range(N):
    if i%2 == 0:
        ta += dish[i][1]
        # ao -= dish[i][2]
    else:
        ao += dish[i][2]
        # ta -= dish[i][1]
print(ta-ao)