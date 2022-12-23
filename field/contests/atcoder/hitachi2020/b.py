A,B,M = map(int,input().split())
ref = list(map(int,input().split()))
mic = list(map(int,input().split()))

ans = min(ref) + min(mic)

for _ in range(M):
    x,y,c = map(int,input().split())
    ans = min(ans, ref[x-1] + mic[y-1] - c)
print(ans)