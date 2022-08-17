from sys import argv
from testcase import TestCase

DR = [1, 0, -1, 0]
DC = [0, 1, 0, -1]


def usage():
    print("python judge.py [testdata_file_path] [output_file_path]")


def inside(pos, size):
    return 0 <= pos < size


def calc_connected_component_size(has_machine, i, j):
    n = len(has_machine)
    visited = [[False] * n for _ in range(n)]
    queue = [(i, j)]
    visited[i][j] = True
    pos = 0
    while pos < len(queue):
        cr, cc = queue[pos]
        for dir in range(4):
            nr = cr + DR[dir]
            nc = cc + DC[dir]
            if inside(nr, n) and inside(nc, n) and not visited[nr][nc] and has_machine[nr][nc]:
                queue.append((nr, nc))
                visited[nr][nc] = True
        pos += 1
    return pos


def error(message):
    raise RuntimeError("[ERROR] " + message)


def judge(tc, output):
    if len(output) != tc.T:
        error("the number of output lines is not %d" % (tc.T,))

    money = 1
    next_price = 1
    veges = [[0] * tc.N for _ in range(tc.N)]
    disappear_on = [[-1] * tc.N for _ in range(tc.N)]
    vege_idx = 0
    has_machine = [[False] * tc.N for _ in range(tc.N)]
    num_machine = 0
    for day, row in enumerate(output):
        if len(row) == 4:
            if not(inside(row[0], tc.N) and inside(row[1], tc.N)):
                error("Day-%d invalid coordinate : (%d %d)" % (day, row[0], row[1]))
            if not(inside(row[2], tc.N) and inside(row[3], tc.N)):
                error("Day-%d invalid coordinate : (%d %d)" % (day, row[2], row[3]))
            if not has_machine[row[0]][row[1]]:
                error("Day-%d invalid move : origin (%d, %d) doesn't have a machine" % (day, row[0], row[1]))
            if (row[0], row[1]) != (row[2], row[3]) and has_machine[row[2]][row[3]]:
                error("Day-%d invalid move : destination (%d, %d) has a machine" % (day, row[2], row[3]))
            has_machine[row[0]][row[1]] = False
            has_machine[row[2]][row[3]] = True
        elif len(row) == 2:
            if not(inside(row[0], tc.N) and inside(row[1], tc.N)):
                error("Day-%d invalid coordinate : (%d %d)" % (day, row[0], row[1]))
            if money < next_price:
                error("Day-%d invalid purchase : money is not enough : money:%d price:%d" % (day, money, next_price))
            if has_machine[row[0]][row[1]]:
                error("Day-%d invalid purchase : position (%d, %d) has a machine" % (day, row[0], row[1]))
            has_machine[row[0]][row[1]] = True
            num_machine += 1
            money -= next_price
            next_price = (num_machine + 1) ** 3
        elif len(row) == 1:
            if row[0] != -1:
                error("Day-%d invalid output" % (day,))
        else:
            error("Day-%d invalid output" % (day,))

        # vegetables appearance
        while vege_idx < tc.M and tc.veges[vege_idx].s == day:
            vege = tc.veges[vege_idx]
            veges[vege.r][vege.c] = vege.v
            disappear_on[vege.r][vege.c] = vege.e
            vege_idx += 1

        # harvest
        for i in range(tc.N):
            for j in range(tc.N):
                if veges[i][j] != 0 and has_machine[i][j]:
                    money += veges[i][j] * calc_connected_component_size(has_machine, i, j)
                    veges[i][j] = 0

        # disappear
        for i in range(tc.N):
            for j in range(tc.N):
                if disappear_on[i][j] == day:
                    veges[i][j] = 0

    return money


def main():
    if len(argv) != 3:
        usage()
        exit(1)
    with open(argv[1]) as in_file:
        tc = TestCase(input=in_file)
    with open(argv[2]) as out_file:
        output = []
        for i, row in enumerate(out_file):
            try:
                output.append(list(map(int, row.split())))
            except Exception:
                error("Day-%d invalid output : %s" % (i, row))
    score = judge(tc, output)
    print("%d" % score)


if __name__ == '__main__':
    main()
