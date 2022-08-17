T = int(input())

for _ in range(T):
    N = int(input())
    LR = [list(map(int,input().split())) for _ in range(N)]

    # 昇順降順を入れ替える場合はlambda式の正負を反転
    LR.sort(key=lambda x:(x[0],x[1]))
    check = set()

    for lr in LR:
        l,r = lr
        for i in range(l,r+1):
            if i not in check:
                check.add(i)
                break
        else:
            print("No")
            break
        
    else:
        print("Yes")
