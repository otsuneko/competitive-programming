N =int(input())

seen = set()
nums = set([i for i in range(1,2*N+2)])

while 1:

    ans = list(nums-seen)[0]
    seen.add(ans)

    print(ans,flush = True)

    fb =int(input())
    seen.add(fb)
    if fb == 0:
        break

