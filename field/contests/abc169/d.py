n = int(input())

if n==1:
    print(0);exit()
#素因数分解して、指数からいくつまで加算できるか算出すればよい
def factorization(n):
    arr = []
    temp = n
    for i in range(2, int(-(-n**0.5//1))+1):
        if temp%i==0:
            cnt=0
            while temp%i==0:
                cnt+=1
                temp //= i
            arr.append([i, cnt])

    if temp!=1:
        arr.append([temp, 1])

    if arr==[]:
        arr.append([n, 1])

    return arr

li = factorization(n)
ans = 0
for f in li:
    f = f[1]
    for i in range(1,f+1):
        if i>f:
            break
        f-=i
        ans+=1
print(ans)
        


