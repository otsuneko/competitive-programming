from collections import defaultdict
dict = defaultdict(int)

N = int(input())
A = list(map(int,input().split()))
B = list(map(int,input().split()))
C = list(map(int,input().split()))

for i in range(N):
    dict[B[C[i]-1]] += 1

ans = 0
for a in A:
    ans += dict[a]

print(ans)