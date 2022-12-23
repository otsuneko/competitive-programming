import math

T = int(input())
L,X,Y = map(int,input().split())
Q = int(input())
for _ in range(Q):
    E = int(input())
    angle = 2 * math.pi * E/T
    Ey = -L*math.sin(angle)/2
    Ez = L*(1-math.cos(angle))/2
    diff_xy = math.sqrt(X**2 + (Ey-Y)**2)
    diff_z = Ez
    ans = math.degrees(math.atan2(diff_z, diff_xy))
    print(ans)