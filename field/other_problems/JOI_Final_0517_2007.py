import itertools
while 1:
    n,k = map(int,input().split())

    if [n,k] == [0,0]:
        break

    card = [int(input()) for i in range(k)]
    card.sort()
    check = set(card)
    ans = 0
    if card[0] == 0:
        for i in range(1,k):
            tmp = card[i]
            cnt = 0
            zero_used = False
            while tmp in check or zero_used == False:
                if tmp not in check:
                    zero_used = True
                tmp += 1
                cnt += 1
            ans = max(ans,cnt)
    else:
        for i in range(k):
            tmp = card[i]
            cnt = 0
            while tmp in check:
                tmp += 1
                cnt += 1
            ans = max(ans,cnt)

    print(ans)