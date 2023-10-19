N = int(input())
S = input()

cumsum_W = [0]*(N+1)
cumsum_E = [0]*(N+1)

for i in range(N):
    cumsum_W[i+1] = cumsum_W[i] + (1 if S[i] == "W" else 0)
    cumsum_E[i+1] = cumsum_E[i] + (1 if S[i] == "E" else 0)

ans = 10**18
for i in range(N):
    change = cumsum_W[i] + (cumsum_E[N]-cumsum_E[i+1])
    ans = min(ans, change)
print(ans)