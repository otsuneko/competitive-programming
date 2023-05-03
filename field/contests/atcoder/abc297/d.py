A,B = map(int,input().split())

ans = 0
while A != B:
    if A > B:
        cnt = -(-(A-B)//B)
        A -= B*cnt
        ans += cnt
    else:
        cnt = -(-(B-A)//A)
        B -= A*cnt
        ans += cnt
    
print(ans)