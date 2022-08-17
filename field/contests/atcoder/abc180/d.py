X,Y,A,B = map(int,input().split())

strength = X
ans = 0
while A*X <= X+B and A*X < Y:
    X *= A
    ans += 1

ans = ans + (Y-X)//B if (Y-X)%B else ans + (Y-X)//B-1
print(ans)

# strength = X
# ans = 0
# while 1:
#     if strength*A > strength+B:
#         ans += (Y-strength)//B if (Y-strength)%B else (Y-strength)//B-1
#         break
#     else:
#         strength = strength*A
#         if strength >= Y:
#             break
#         else:
#             ans += 1
# print(ans)