N = int(input())

ans = []
for _ in range(100):
    N2 = N
    power = 0
    while N2 >= 3:
        N2 //= 3
        power += 1

    if N - 3**power > 3**(power+1) - N:
        ans.append(3**(power+1))
        N = 3**(power+1) - N
    else:
        ans.append(3**(power))
        N = N - 3**power
print(ans)