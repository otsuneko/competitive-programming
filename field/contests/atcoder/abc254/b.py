N = int(input())

print(1)
li = []
for i in range(N-1):
    new_li = [1]
    for j in range(len(li)-1):
        new_li.append(li[j]+li[j+1])
    new_li.append(1)
    print(*new_li)
    li = new_li