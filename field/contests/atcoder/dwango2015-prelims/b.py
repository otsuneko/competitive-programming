S = input()

li = [1]
for i in range(2,10**5+1):
    li.append(li[-1]+i)

ans = 0
idx = 0
while idx < len(S):
    if S[idx] != "2" or idx == len(S)-1:
        idx += 1
        continue
    
    cnt = 0
    while idx < len(S)-1:
        if S[idx:idx+2] == "25":
            cnt += 1
            idx += 2
        else:
            idx += 1
            break
    if cnt:
        ans += li[cnt-1]

print(ans)