import math
t, N = map(int,input().split())

no_exist = []
cnt = 0
for i in range(1,101):
    n = i*(100+t)//100
    if n - cnt != i:
        no_exist.append(i+cnt)
        cnt += 1

l=len(no_exist)
print(no_exist[N%l-1] + (N-1)//l * (100+t))