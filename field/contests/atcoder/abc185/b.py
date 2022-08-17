N,M,T = map(int,input().split())

now = 0
battery = N
for _ in range(M):
    A,B = map(int,input().split())
    battery = max(0,battery-(A-now))
    if battery == 0:
        print("No")
        exit()
    battery = min(N,battery+(B-A))
    now = B

battery = max(0,battery-(T-now))
print(["No","Yes"][battery > 0])