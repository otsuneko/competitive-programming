X,Y,A,B,C = map(int,input().split())

pos = sorted([X,Y])
rect = sorted([A,B,C], reverse=True)
l1 = (rect[0]+pos[0]-1)//pos[0]

