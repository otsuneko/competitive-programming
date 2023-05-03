N = int(input())
S = input()

ans = True
cnt = 0
for s in S:
    if s == "o":
        cnt += 1
    elif s == "x":
        ans = False

print(["No","Yes"][ans and cnt > 0])