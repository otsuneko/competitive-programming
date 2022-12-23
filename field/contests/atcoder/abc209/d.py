
# binary tree node
class Node:
	# Constructor to create new node
	def __init__(self, data):
		self.data = data
		self.left = self.right = None

# This function returns pointer to LCA of
# two given values n1 and n2.
def LCA(root, n1, n2):
	
	# Base case
	if root is None:
		return None

	# If either n1 or n2 matches with root's
	# key, report the presence by returning
	# root
	if root.data == n1 or root.data == n2:
		return root
	if root.data == None or root.data == None:
		return None

	# Look for keys in left and right subtrees
	left = LCA(root.left, n1, n2)
	right = LCA(root.right, n1, n2)

	if left is not None and right is not None:
		return root

	# Otherwise check if left subtree or
	# right subtree is LCA
	if left:
		return left
	else:
		return right

# function to find distance of any node
# from root
def findLevel(root, data, d, level):
	
	# Base case when tree is empty
	if root is None:
		return

	# Node is found then append level
	# value to list and return
	if root.data == data:
		d.append(level)
		return

	findLevel(root.left, data, d, level + 1)
	findLevel(root.right, data, d, level + 1)

# function to find distance between two
# nodes in a binary tree
def findDistance(root, n1, n2):
	
	lca = LCA(root, n1, n2)
	
	# to store distance of n1 from lca
	d1 = []
	
	# to store distance of n2 from lca
	d2 = []

	# if lca exist
	if lca:
		
		# distance of n1 from lca
		findLevel(lca, n1, d1, 0)
		
		# distance of n2 from lca
		findLevel(lca, n2, d2, 0)
		return d1[0] + d2[0]
	else:
		return -1

import sys
sys.setrecursionlimit(10**7)
def dfs(root):
    if len(adj[root.data]) > 1:
        root.left = Node(adj[root.data])

N,Q = map(int, input().split())
LV = (N-1).bit_length()
prv = [None]*N
G = [None]*N
adj = [[] for _ in range(N)]
for i in range(N-1):
    a,b = map(int, input().split())
    a,b = a-1,b-1
    adj[a].append(b)

root = Node(0)

for _ in range(Q):
    c,d = map(int,input().split())
    c,d = c-1,d-1

### basic answer ###
# from collections import deque

# def bfs(dist):
#     queue = deque()
#     queue.append(0)
#     while queue:
#         v1 = queue.popleft()
#         for v2 in adj[v1]:
#             if dist[v2] != -1:
#                 continue
#             dist[v2] = dist[v1] + 1
#             queue.append(v2)

# N,Q = map(int, input().split())
# adj = [[] for _ in range(N)]
# for _ in range(N-1):
#     a,b = map(int, input().split())
#     a,b = a-1,b-1
#     adj[a].append(b)
#     adj[b].append(a)

# dist = [-1] * N
# dist[0] = 0

# ans = bfs(dist)

# for _ in range(Q):
#     c,d = map(int,input().split())
#     c,d = c-1,d-1
#     dis = abs(dist[c]-dist[d])
#     if dis%2:
#         print("Road")
#     else:
#         print("Town")