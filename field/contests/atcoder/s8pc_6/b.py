N = int(input())
goods = []
pos_A = []
pos_B = []
for _ in range(N):
    a,b = map(int,input().split())
    goods.append((a,b))
    pos_A.append(a)
    pos_B.append(b)
pos_A.sort()
pos_B.sort()

enter = pos_A[N//2]
out = pos_B[N//2]

ans = 0
for i in range(N):
    ans += abs(out-goods[i][1]) + abs(goods[i][1] - goods[i][0]) + abs(goods[i][0] - enter)

print(ans)