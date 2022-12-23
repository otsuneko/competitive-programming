N,K = map(int,input().split())
D = set(list(map(int,input().split())))
keta = [0]*5

ans = 10**18
for keta[0] in range(10):
    for keta[1] in range(10):
        for keta[2] in range(10):
            for keta[3] in range(10):
                for keta[4] in range(10):
                    leading = 0
                    for i in range(5):
                        if keta[i] == 0:
                            leading += 1
                        else:
                            break
                    price = ""
                    for i in range(5):
                        price += str(keta[i])
                    
                    price = int(price)
                    if price >= N and len(set(keta[leading:]) & D) == 0:
                        ans = min(ans,price)
print(ans)