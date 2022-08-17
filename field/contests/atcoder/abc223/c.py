N = int(input())

sen = []
time = 0
for _ in range(N):
    A,B = map(int,input().split())
    sen.append([A,B])
    time += A/B

time /= 2

x = 0
t = 0
for A,B in sen:
    if t + A/B < time:
        x += A
        t += A/B
    else:
        x += B * (time-t)
        break
print(x)