from collections import defaultdict
N = int(input())
check = [0]*N
for _ in range(N):
    a = int(input())
    check[a-1] += 1

deleted = -1
overwrite = -1
for i in range(N):
    if check[i] == 0:
        deleted = i+1
    elif check[i] == 2:
        overwrite = i+1

if overwrite != -1:
    print(overwrite,deleted)
else:
    print("Correct")
