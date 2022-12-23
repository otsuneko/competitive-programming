import math

def rotate(x,y,angle):
    #回転中心の座標(原点の場合は0)
    center_x = 0
    center_y = 0
    #回転角度(radian)
    angle = math.radians(angle)
    #回転後の座標 
    X = math.cos(angle) * (x - center_x) - math.sin(angle) * (y - center_y) + center_x
    Y = math.sin(angle) * (x - center_x) + math.cos(angle) * (y - center_y) + center_y

    return X,Y

A,B,H,M = map(int,input().split())

h_d = (H%12)*30 + M*0.5
m_d = M*6

X1,Y1 = rotate(0,A,h_d)
X2,Y2 = rotate(0,B,m_d)

print(math.sqrt((X1-X2)**2 + (Y1-Y2)**2))


#degree
# h_degree = h*30+m*0.5
# m_degree = m*6
# degree = min(360-abs(h_degree-m_degree),abs(h_degree-m_degree))

# ans = (a**2+b**2-2*a*b*math.cos(math.radians(degree)))**0.5
# print(ans)