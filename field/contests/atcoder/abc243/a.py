V,A,B,C =map(int,input().split())

i = 0
while 1:
    if i%3==0:
        if V >= A:
            V-=A
        else:
            print("F")
            exit()  
    elif i%3==1:
        if V >= B:
            V-=B
        else:
            print("M")
            exit()
    elif i%3==2:
        if V >= C:
            V-=C
        else:
            print("T")
            exit()
    i+=1