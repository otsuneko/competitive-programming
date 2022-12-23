N =int(input())
A = list(map(int,input().split()))

stack = []
ans = 0
for a in A:
    if stack and stack[-1][0] == a:
        if stack[-1][1]+1 == a:
            stack.pop()
            ans -= a-1
        else:
            stack[-1][1] += 1
            ans += 1
    else:
        stack.append([a,1])
        ans += 1

    print(ans)