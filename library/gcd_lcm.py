import math

def gcd(a,b):
    return math.gcd(a,b)

def gcd_list(list_n):
    x = list_n.pop(0)
    for i in range(len(list_n)):
        x = math.gcd(x,list_n[i])
    return x

def lcm(a,b):
    return a*b//math.gcd(a,b)

def lcm_list(list_n):
    x = list_n.pop(0)
    for i in range(len(list_n)):
        x = x*list_n[i]//math.gcd(x,list_n[i])
    return x
