N,K = map(int,input().split())
for _ in range(N):
    a,b,c = map(int,input().split())
    for i in range(a):
        bisect.insort(arr,b + i*c)
print(arr[K-1])