N = int(input())
if N%2:
    print(0)
    exit()

p5 = 5
ans = 0
while p5 <= N:
    ans += (N // p5) // 2 # 5,25,50の倍数であっても、N!!に下1桁が5のものは登場しないから個数は半分
    p5 *= 5

print(ans)