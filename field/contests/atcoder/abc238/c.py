mod = 998244353
N = int(input())

ans = 0

if len(str(N))==1:
    print((1+N)*N//2)
    exit()

su = 0
for keta in range(1,len(str(N))):
    ma = int("9"+"0"*(keta-1))
    su += ((1+ma)*ma//2)%mod
    # print(su)

a = 10**(len(str(N))-1)
b = N-a+1
ans = (su + (b)*(b+1)//2)%mod
print(ans)