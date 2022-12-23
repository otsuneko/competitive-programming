W =int(input())

li = []
for i in range(1,100):
    li.append(i)

for i in range(100,10000,100):
    li.append(i)

for i in range(10000,1000001,10000):
    li.append(i)

print(len(li))
print(*li)