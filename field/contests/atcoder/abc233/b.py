L,R =map(int,input().split())
L,R = L-1,R-1
S = input()

print(S[:L] + S[L:R+1][::-1] + S[R+1:])