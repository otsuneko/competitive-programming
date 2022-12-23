# ダブリング
N,K = map(int, input().split())
A = list(map(int, input().split()))

# 2**60 ≒ 10**18
nxt = [[-1]*N for _ in range(61)]
cost = [[-1]*N for _ in range(61)]

for i in range(N):
    # iの1つ先のidx
    nxt[0][i] = (i+A[i])%N
    # iのコスト
    cost[0][i] = A[i]

for loop in range(1,61):
    for i in range(N):
        nxt[loop][i] = nxt[loop-1][nxt[loop-1][i]]
        cost[loop][i] = cost[loop-1][nxt[loop-1][i]] + cost[loop-1][i]

ans = 0
i = 0
for loop in range(61):
    if ((K >> loop) & 1) == 1:
        ans += cost[loop][i]
        i = nxt[loop][i]
print(ans)


# フロイドの循環検出
# class Node:
#     def __init__(self, val):
#         self.val = val
#         self.next = None
#         self.prev = None

# # サイクル(閉路)があるか判定
# def hasCycle(head):
#    fast = slow = head
#    while fast and fast.next:
#        fast = fast.next.next
#        slow = slow.next
#        if fast == slow:
#            return True
#    return False

# # サイクル(閉路)の開始地点を探索
# def findCycleStart(head):
#    fast = slow = head
#    while fast and fast.next:
#        fast = fast.next.next
#        slow = slow.next
#        if fast == slow:
#            fast = head
#            while fast != slow:
#                fast = fast.next
#                slow = slow.next
#            return fast.val
#    return None

# # サイクルのループ長を探索
# def findCycleLen(head):
#    fast = slow = head
#    count = 0
#    while fast and fast.next:
#        count += 1
#        fast = fast.next.next
#        slow = slow.next
#        if fast == slow:
#            return count
#    return False

# N,K = map(int, input().split())
# A = list(map(int, input().split()))

# nodes = [Node(i) for i in range(N)]
# for i in range(N):
#     nodes[i].next = nodes[(i+A[i])%N]

# # サイクル開始位置と1サイクルの長さを求める
# cycleStart = findCycleStart(nodes[0])
# cycleLen = findCycleLen(nodes[cycleStart])

# # 1サイクル分の合計
# cycleTotal = A[cycleStart]
# idx = nodes[cycleStart].next.val
# while idx != cycleStart:
#     cycleTotal += A[idx]
#     idx = nodes[idx].next.val

# ans = 0
# # サイクル開始地点までの合計
# idx = 0
# while idx != cycleStart:
#     ans += A[idx]
#     idx = nodes[idx].next.val
#     K -= 1
#     if K == 0:
#         print(ans)
#         exit()

# # サイクル内ループの合計
# ans += cycleTotal * (K // cycleLen)
# K %= cycleLen

# # サイクル内ループの余り分の合計
# idx = cycleStart
# while K > 0:
#     ans += A[idx]
#     idx = nodes[idx].next.val
#     K -= 1
# print(ans)


# 普通の循環検出
# N,K =map(int,input().split())
# A =list(map(int,input().split()))

# X = 0
# li = []
# li_mod = []
# seen = set()
# for _ in range(K):
#     li.append(A[X%N])
#     li_mod.append(X%N)
#     seen.add(X%N)
#     X += A[X%N]
#     if X%N in seen:
#         break

# if X%N in li_mod:
#     ini = li_mod.index(X%N)
# else:
#     ini = 0
# loop = len(li_mod)-ini

# div = (K-ini)//loop
# mod = (K-ini)%loop
# print(ini,loop,div,mod)

# su_ini = sum(li[:ini])
# print(li[:ini])
# su_loop = sum(li[ini:ini+loop])*div
# su_mod = sum(li[ini:ini+mod])
# ans = su_ini + su_loop + su_mod
# print(ans)