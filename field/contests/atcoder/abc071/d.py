N = int(input())
S = [list(input()) for _ in range(2)]
mod = 10**9+7

ans = 1
i = 0
if S[0][0] == S[1][0]:
    ans = 3
    i += 1
else:
    ans = 6
    i += 2

while i < N:
    # ドミノが縦向きの場合
    if S[0][i] == S[1][i]:
        # 1個左のドミノが縦向きの場合
        if S[0][i-1] == S[1][i-1]:
            ans = ans * 2 % mod
        i += 1
    # ドミノが横向きの場合
    else:
        # 1個左のドミノが縦向きの場合
        if S[0][i-1] == S[1][i-1]:
            ans = ans * 2 % mod
        else:
            ans = ans * 3 % mod
        i += 2

print(ans)