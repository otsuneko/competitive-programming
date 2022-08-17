S,T,X = map(int,input().split())

if S > T:
    if 0 <= X < T or S <= X < 24:
        print("Yes")
    else:
        print("No")
else:
    if S <= X < T:
        print("Yes")
    else:
        print("No")