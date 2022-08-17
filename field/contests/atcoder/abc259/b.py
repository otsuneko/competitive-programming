import math

a,b,d = map(int,input().split())

#回転前の座標
x = a
y = b
#回転中心の座標(原点の場合は0)
center_x = 0
center_y = 0
#回転角度(radian)
angle = math.pi*2 * d/360
#回転後の座標 
X = math.cos(angle) * (x - center_x) - math.sin(angle) * (y - center_y) + center_x
Y = math.sin(angle) * (x - center_x) + math.cos(angle) * (y - center_y) + center_y

print(X,Y)
