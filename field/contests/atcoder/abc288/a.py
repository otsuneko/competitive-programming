N = int(input())
num = [list(map(int,input().split())) for _ in range(N)]

for a,b in num:
    print(a+b)