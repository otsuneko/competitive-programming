N,M = map(int,input().split())
A = set(list(map(int,input().split())))
B = set(list(map(int,input().split())))
C = A & B
ans = sorted(list(C))
print(*ans)