import sys
input = lambda: sys.stdin.readline().rstrip()
INF = 10**18

from collections import defaultdict

def solve(N,sodas):

    created = [(0,0)]
    remaining = set()
    pos_list = set()
    MAX = 10**9
    for a,b in sodas:
        remaining.add((a,b))
        pos_list.add((a,b))
    C = 0

    ans = []

    # 格子状に飲料を作成
    step = MAX//25
    src_dict = defaultdict(set)
    dst_dict = defaultdict(set)
    for a in range(0,MAX,step):
        for b in range(step,MAX,step):
            created.append((a,b))
            if (a,b) in remaining:
                remaining.remove((a,b))
            ans.append((a, max(0,b-step), a, b))
            src_dict[(a, b)].add((a, max(0,b-step)))
            dst_dict[(a, max(0,b-step))].add((a, b))
            C += step
        if a >= MAX-step:
            continue
        b = 0
        created.append((a+step,b))
        if (a,b) in remaining:
            remaining.remove((a,b))
        ans.append((a, b, a+step, b))
        src_dict[(a+step, b)].add((a,b))
        if a+step+step < MAX:
            dst_dict[(a, b)].add((a+step, b))
        C += step

    # print(created, file=sys.stderr)
    # print(len(created), file=sys.stderr)
    # print(ans, file=sys.stderr)

    # 最も近いやつ飲料から作成
    for dst_a,dst_b in sodas:
        ma_a,ma_b = 0,0
        for src_a,src_b in created:
            if dst_a >= src_a and dst_b >= src_b and src_a >= ma_a and src_b >= ma_b:
                ma_a, ma_b = src_a, src_b

        if [ma_a,ma_b] == [dst_a,dst_b]:
            continue
        created.append((dst_a,dst_b))
        if (dst_a,dst_b) in remaining:
            remaining.remove((dst_a,dst_b))
        ans.append((ma_a, ma_b, dst_a,dst_b))
        src_dict[(dst_a,dst_b)].add((ma_a, ma_b))
        dst_dict[(ma_a, ma_b)].add((dst_a,dst_b))
        C += dst_a - ma_a + dst_b - ma_b

    # 複数の飲料の原料になっている飲料は、より作成先の飲料に近い中間飲料を作成する
    add = []
    for src_a, src_b, dst_a, dst_b in ans:
        if len(dst_dict[(src_a, src_b)]) == 1:
            continue
        for dst_a,dst_b in dst_dict[(src_a, src_b)]:
            add.append((dst_a, src_b, dst_a, dst_b))

    # 一度もsourceになっていない飲料は削除可能
    # while 1:
    # del_list = []
    # for key,val in dst_dict.items():
    #     src_a,src_b = key
    #     dsts = val
    #     if len(dst_dict[(src_a,src_b)]) == 0 and (src_a,src_b) not in pos_list:
    #         del_list.append((src_a, src_b, dst_a, dst_b))

    # for d in del_list:
    #     ans.remove(d)

    print(len(remaining), file=sys.stderr)
    print(C, file=sys.stderr)
    return (ans+add)[:5000]

def main():
    N = int(input())
    sodas = [list(map(int,input().split())) for _ in range(N)]
    ans = solve(N,sodas)
    print(len(ans))
    for a in ans:
        print(*a)

main()
