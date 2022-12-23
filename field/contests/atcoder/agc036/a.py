S = int(input())
v = 10**9
x = (v-S%v)%v
y = (S+x)//v
print(0,0,v,1,x,y)