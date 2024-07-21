import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

import sys,pypyjit
sys.setrecursionlimit(10**7)
pypyjit.set_param('max_unroll_recursion=0')

class Node(object):
   def __init__(self) -> None:
       self.children = {}
       self.value = 0

def find(node, key):
    for c in key:
        if c not in node.children:
            return False
        node = node.children[c]
    return node.value

def insert(node, key):
    for c in key:
        if c not in node.children:
            node.children[c] = Node()
        node = node.children[c]
        node.value += 1


N = int(input())
S = list(map(str,input().split()))

def dfs(node, s, idx):

    res = node.value
    for c2 in node.children:
        if idx < len(s) and s[idx] == c2:
            res += dfs(node.children[s[idx]], s, idx+1)
    return res

root = Node()
ans = 0
for i in range(N):
    ans += dfs(root, S[i], 0)

    node = root
    for c in S[i]:
        insert(node,c)
        node = node.children[c]
print(ans)
