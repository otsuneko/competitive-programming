dir = ["U","D","R","L"]
sx,sy,tx,ty = map(int, input().split())

ans = ""

dy,dx = ty-sy,tx-sx
ans += "U"*dy + "R"*dx + "D"*dy + "L"*dx
ans += "L" + "U"*(dy+1) + "R"*(dx+1) + "D" + "R" + "D"*(dy+1) + "L"*(dx+1) + "U"
print(ans)