N,X,Y = map(int,input().split())

red = [0]*10
blue = [0]*10
red[N-1] = 1

while sum(red[1:]) != 0:
    for i in range(9,0,-1):
        if red[i] > 0:
            red[i-1] += red[i]
            blue[i] += X*red[i]
            red[i] = 0
    
    for i in range(9,0,-1):
        if blue[i] > 0:
            red[i-1] += blue[i]
            blue[i-1] += Y*blue[i]
            blue[i] = 0

# print(red,blue)
print(blue[0])