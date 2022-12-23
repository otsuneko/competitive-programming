def digsum(n):
    res = 0
    while n > 0:
        res += n%10
        n //= 10
    
    return res

N = int(input())

cand_x = []


ans_x = 10**18
ans_m = 0
for x in cand_x:
    x = int(x)
    m = digsum(2*x)
    if m > ans_m:
        ans_m = m
print(ans_m)
