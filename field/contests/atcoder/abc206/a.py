import math
N = int(input())

mon = math.floor(1.08*N)

if mon == 206:
    print("so-so")
elif mon > 206:
    print(":(")
else:
    print("Yay!")