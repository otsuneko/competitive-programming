import itertools

N = int(input())
S = input()

com = ["A","B","X","Y"]
ans = 10**18
for prod in itertools.product(com,repeat=4):
    L = "".join(prod[:2])
    R = "".join(prod[2:])
    S2 = S.replace(L,"L")
    S3 = S2.replace(R,"R")
    ans = min(ans,len(S3))

print(ans)