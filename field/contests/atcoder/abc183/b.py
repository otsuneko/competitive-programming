Sx,Sy,Gx,Gy = map(int,input().split())

a = (Gy+Sy)/(Gx-Sx)
b = Gy - a*Gx

print(-b/a)