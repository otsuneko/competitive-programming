# ランレングス圧縮
N = int(input())
S = list(input())

all = (N-1)*N//2

prev = S[0]
cnt = 0
for i in range(1,N):
    if S[i] == prev:
        cnt += 1
    else:
        all -= (cnt+1)*cnt//2
        cnt = 0
        prev = S[i]
all -= (cnt+1)*cnt//2

print(all)

# original answer
# N = int(input())
# S = input()

# o_idx = x_idx = -1
# closest = [-1]*N

# for i in reversed(range(N)):
#     if S[i] == "o":
#         o_idx = i
#     else:
#         x_idx = i
    
#     if i < N-1:
#         if S[i] == "o":
#             closest[i] = x_idx
#         else:
#             closest[i] = o_idx

# ans = 0
# for i in range(N-1):
#     if closest[i] != -1:
#         ans += (N-i) - (closest[i]-i)
# print(ans)