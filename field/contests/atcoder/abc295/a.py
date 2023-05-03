N = int(input())
W = input().split()

for w in W:
    if w in ["and","not","that","the","you"]:
        print("Yes")
        exit()
print("No")
