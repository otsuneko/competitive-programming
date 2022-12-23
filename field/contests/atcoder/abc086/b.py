a,b = map(str,input().split())
n = int(a+b)
if n**(0.5) == int(n**(0.5)):
    print("Yes")
else:
    print("No")