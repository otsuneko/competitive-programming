N,K = map(int,input().split())

print(min(N%K, abs(N%K-K)))