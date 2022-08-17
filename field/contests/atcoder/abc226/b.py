N = int(input())
s = set()
for _ in range(N):
    L,*A = map(int,input().split())
    s.add(tuple(A))

print(len(s))