import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

N = int(input())
A = list(map(int,input().split()))
nodes = [Node(i) for i in range(N)]

start = 0
for i in range(N):
    pre,nxt = A[i]-1,i
    if A[i] == -1:
        start = i
    else:
        nodes[pre].prev = pre
        nodes[pre].next = nxt

# for i in range(N):
#     print(vars(nodes[i]))

ans = [start+1]
cur = start
while len(ans) < N:
    cur = nodes[cur].next
    ans.append(cur+1)
print(*ans)