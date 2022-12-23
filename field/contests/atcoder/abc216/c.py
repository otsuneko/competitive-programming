N = int(input())

ans = []

while N > 0:
    if N%2:
        ans.append("A")
        N -= 1
    else:
        ans.append("B")
        N//=2

print("".join(ans[::-1]))
