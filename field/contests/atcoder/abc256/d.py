N = int(input())
enter = []
exit = []
for _ in range(N):
    l,r = map(int,input().split())
    enter.append(l)
    exit.append(r)

last_exit = max(exit)
table = [0] * (last_exit + 1)

for i in range(N):
  table[enter[i]] += 1
  table[exit[i]] -= 1

# シミュレート(累積和)
for i in range(1, last_exit):
  table[i] += table[i - 1]

ans = []
start = end = 0
flg = False
for i in range(1,last_exit+1):
    if table[i] > 0 and flg == False:
        start = i
        flg = True
    if table[i] < 1 and flg == True:
        flg = False
        ans.append((start,i))   

# print(table)
for a in ans:
    print(*a)