N = int(input())
name = [list(map(str,input().split())) for _ in range(N)]

check = set()
for n in name:
    if (n[0],n[1]) in check:
        print("Yes")
        exit()
    check.add((n[0],n[1]))
print("No")