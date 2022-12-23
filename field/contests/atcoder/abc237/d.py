# Pythonで提出!!
import sys
sys.setrecursionlimit(10**7)

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

# 行きがけ/通りがけ/帰りがけの順序を出力
def dfs(s):
    if s:
        order[0].append(s.val) # 行きがけ
        dfs(s.prev)
 
        order[1].append(s.val) # 通りがけ

        dfs(s.next)
        order[2].append(s.val) # 通りがけ

N =int(input())
S = input()

nodes = [Node(i) for i in range(N+1)]
for i in range(len(S)):
    if S[i] == "R":
        nodes[i].next = nodes[i+1]
    else:
        nodes[i].prev = nodes[i+1]

order = [[] for _ in range(3)]
dfs(nodes[0])
print(order)
print(*order[1])


###別解###
# from collections import deque
# N =int(input())
# S = input()

# d = deque([str(len(S))])
# for i in range(len(S)-1,-1,-1):
#     if S[i] == "R":
#         d.appendleft(str(i))
#     else:
#         d.append(str(i))

# print(" ".join(d))
