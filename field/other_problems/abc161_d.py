from collections import deque
k = int(input())
num_li = deque()
for i in range(1,10):
    num_li.append(i)
while True:
    l = len(num_li)
    if l >= k:
        print(num_li[k-1]);exit()
    else:
        k -= l
        for i in range(l):
            left = num_li.popleft()
            last = left%10
            add1,add2,add3 = 10*left+last-1,10*left+last,10*left+last+1
            if 0 < last < 9:
                num_li.append(add1)
                num_li.append(add2)
                num_li.append(add3)
            elif last == 0:
                num_li.append(add2)
                num_li.append(add3)
            else:
                num_li.append(add1)
                num_li.append(add2)
