def f(i, m, s, memoize):

    # End of the string.
    if (i == len(s)):
        return 0

    # If already calculated, return
    # the stored value.
    if (memoize[i][m] != -1):
        return memoize[i][m]

    # Converting into integer.
    x = ord(s[i]) - ord('0')

    # Increment result by 1, if current digit
    # is divisible by 3 and sum of digits is
    # divisible by 673.
    # And recur for next index with new modulo.
    ans = (((x + m) % 673 == 0 and x % 3 == 0) +
        f(i + 1, (m + x) % 673, s, memoize))

    memoize[i][m] = ans
    return memoize[i][m]

# Returns substrings divisible by 6.
def countDivBy2019(s):
    n = len(s)

    # For storing the value of all states.
    memoize = [[-1] * 673 for i in range(n + 1)]

    ans = 0
    for i in range(len(s)):
        ans += f(i, 0, s, memoize)

    return ans

S = input()
print(countDivBy2019(S))