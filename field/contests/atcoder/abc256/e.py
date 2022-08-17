# フロイドの循環検出
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

# サイクル(閉路)があるか判定
def hasCycle(head):
    fast = slow = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
        if fast == slow:
            return True
    return False

# サイクル(閉路)の開始地点を探索
def findCycleStart(head):
    fast = slow = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
        if fast == slow:
            fast = head
            while fast != slow:
                fast = fast.next
                slow = slow.next
            return fast.val
    return None

# サイクルのループ長を探索
def findCycleLen(head):
    fast = slow = head
    count = 0
    while fast and fast.next:
        count += 1
        fast = fast.next.next
        slow = slow.next
        if fast == slow:
            return count
    return False

N = int(input())
X = list(map(int,input().split()))
C = list(map(int,input().split()))

nodes = [Node(i) for i in range(N)]
rnodes = [Node(i) for i in range(N)]
for i in range(N):
    X[i] -= 1
    nodes[i].next = nodes[X[i]]
    rnodes[X[i]].next = rnodes[i]

cyclestarts = []
seen = [False]*N
for i in range(N):
    if seen[i] == False:
        s = findCycleStart(nodes[i])
        if i == s:
            cyclestarts.append(i)
        seen[i] = True

ans = 0
seen = [False]*N
for s in cyclestarts:
    if seen[s] == False:
        seen[s] = True
        mi = 10**18
        to = s
        while 1:
            to = nodes[to].next.val
            mi = min(mi,C[to])
            if to == s:
                break
            seen[to] = True
    ans += mi

print(ans)