from collections import deque
N =int(input())
S = list(input())

even = 0
odd = []
for i in range(N-2):
    if S[i:i+3] == ["A","R","C"]:
        cnt = 1
        l = i-1
        r = i+3
        while l >= 0 and r < N:
            if S[l] == "A" and S[r] == "C":
                cnt += 1
            else:
                break
            l -= 1
            r += 1
        if cnt > 1:
            odd.append(cnt)
        else:
            even += cnt

# print(odd,even)
odd.sort()
odd = deque(odd)
ans = 0
remain_odd = sum(odd)
remain_even = even
while remain_odd > 0 and remain_even > 0:
    remain_odd -= 1
    if len(odd) and odd[0] > 0:
        odd[0] -= 1
        if odd[0] == 0:
            odd.popleft()
    remain_even -= 1
    ans += 2

if remain_odd == 0:
    ans += remain_even
elif remain_even == 0:
    cnt = 0
    while sum(odd) != 0:
        for i in range(len(odd)):
            if cnt%2==0 and odd[i] > 0:
                odd[i] -= 1
                ans += 1
                cnt += 1
            elif cnt%2==1 and odd[i] > 0:
                odd[i] = 0
                ans += 1
                cnt += 1

print(ans)
