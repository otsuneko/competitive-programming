import math
a,b,h,m = map(int,input().split())

#degree
h_degree = h*30+m*0.5
m_degree = m*6
degree = min(360-abs(h_degree-m_degree),abs(h_degree-m_degree))

ans = (a**2+b**2-2*a*b*math.cos(math.radians(degree)))**0.5
print(ans)