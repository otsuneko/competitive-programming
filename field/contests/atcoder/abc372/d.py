import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

N = int(input())
H = list(map(int,input().split()))
ans = [0]
stack = []

for i in range(N-2,-1,-1):
    while stack and stack[-1] < H[i+1]:
        stack.pop()
    stack.append(H[i+1])
    ans.append(len(stack))
print(*ans[::-1])
