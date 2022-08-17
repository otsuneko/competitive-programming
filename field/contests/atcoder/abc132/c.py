N = int(input())
D = list(map(int,input().split()))
D.sort()

print(D[N//2]-D[N//2-1])