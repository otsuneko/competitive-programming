#!/usr/bin/env python3
# usage: $ oj generate-input 'python3 generate.py'
# usage: $ oj generate-input --hack-actual=./a.out --hack-expected=./naive 'python3 generate.py'
import random

# generated by oj-template v4.8.1 (https://github.com/online-judge-tools/template-generator)
def main():
    a = random.randint(1, 10 ** 9)  # TODO: edit here
    b = random.randint(1, 1000)  # TODO: edit here
    c = [None for _ in range(b)]
    d = [None for _ in range(b)]
    for i in range(b):
        c[i] = ''.join([random.choice('abcde') for _ in range(random.randint(1, 100))])  # TODO: edit here
        d[i] = random.randint(1, 10 ** 9)  # TODO: edit here
    e = random.randint(1, 10 ** 9)  # TODO: edit here
    print(a, b)
    for i in range(b):
        print(c[i])
        print(d[i], end=' ')
    print(e)

if __name__ == "__main__":
    main()
