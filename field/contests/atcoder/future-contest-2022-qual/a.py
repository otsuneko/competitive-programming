import sys
input = lambda: sys.stdin.readline().rstrip()
import time
import random
import math
from collections import deque

#依存関係にあるタスクが完了されているか
def if_depend_task_finished(task):
    res = True
    for necessary in task_depend_in[task]:
        if task_status[necessary] != 1:
            res = False
            break
    return res

# タスクへのアサインを決定
def assign_member_to_task():
    assign_list = []
    for task_num in priority_tasks:
        if task_status[task_num] != -1 or not if_depend_task_finished(task_num):
            continue
        cand_members = []
        assign_num = 0
        for member_num in range(M):
            if member_status[member_num] == -1:
                cand_members.append([member_num,0]) # [どのメンバーか、要求スキルとの差(w)]
                for k in range(K):
                    skill_gap = task_diff[task_num][k] - member_skill[member_num][k]
                    cand_members[-1][1] += max(0,skill_gap)
            else:
                assign_num += 1
        
        # 全メンバーが何らかのタスクを持っている場合は終了
        if assign_num == M:
            break
 
        final_choice = [-1,0]
        if len(cand_members) > 0:
            cand_members.sort(key=lambda x:(x[1]))
            final_choice = [*cand_members[0]]
        
        if final_choice[0] != -1:
            task_status[task_num] = 0
            member_status[final_choice[0]] = task_num
            estimated_duration = max(1, final_choice[1])
            task_start_and_estimate[final_choice[0]] = [day, estimated_duration]
            assign_list.append(str(final_choice[0]+1) + " " + str(task_num+1))
 
    return assign_list

# あるメンバーの推定スキルを基に計算した工数がどれだけ過去の実所要時間からズレているか計算
def calc_skill_gap(fin_tasks, member_skill):
    gap = 0
    for task_num, duration in fin_tasks:
        w = 0
        for k in range(K):
            w += max(0, task_diff[task_num][k] - member_skill[k])
        w = 1 if w == 0 else w
        # 所要時間が1かつw=0の時は、各diffとskillの差が不明確なのでスキップ
        gap += abs(duration - w)**2
    # MAE → NRMSDに変更
    gap = math.sqrt(gap/len(fin_tasks)) / (max(1,(max_duration - min_duration)))
    return gap

# これまでにあるメンバーが遂行した各タスクの実所要時間を基に
# スキルを乱数でブレさせて、最も実績にフィットするスキルを探索
def recalc_member_skill_random(member, fin_tasks):

    # 現在の推定スキルがどれだけ過去の実績からズレているか計算
    ini_gap = calc_skill_gap(fin_tasks, member_skill[member])

    best_fit_skills = [[ini_gap, [*member_skill[member]]] for _ in range(CAND_NUM)] # [gap, skills]

    # NUM_RANDOM_LOOP回乱択する
    for _ in range(NUM_RANDOM_LOOP):
        # ブレさせたスキルを生成
        member_skill_rand = [[0]*K for _ in range(CAND_NUM)]
        for i in range(CAND_NUM):
            for k in range(K):
                member_skill_rand[i][k] = max(0,best_fit_skills[i][1][k] + random.randint(-1,1))

            # 生成したスキルがどれだけ過去の実績にフィットしているか検証
            gap = calc_skill_gap(fin_tasks, member_skill_rand[i])

            # 過去の実所要時間とのギャップがより少なければ採用
            if gap < best_fit_skills[i][0]:
                best_fit_skills[i][0] = gap
                best_fit_skills[i][1] = [*member_skill_rand[i]]

    best_fit_skills.sort()
    member_skill[member] = [*best_fit_skills[0][1]]

# 各種ステータスの更新
def update_status(finish_members):
    global max_duration, min_duration
    for member_num in finish_members:
        member_num -= 1 # 0-index
        task_num = member_status[member_num]
        task_status[task_num] = 1
        member_status[member_num] = -1
        duration = day - task_start_and_estimate[member_num][0] + 1
        max_duration, min_duration = max(max_duration, duration), min(min_duration, duration)
        finished_tasks[member_num].append((task_num, duration))

        # あるメンバーがこなしたタスクが一定回数になったら、過去の実績を基にスキルを乱択調整
        finish_task_num = len(finished_tasks[member_num])
        NOW = time.time()
        if (NOW-START) > TIME_LIMIT:
            continue
        if (finish_task_num < M and finish_task_num%2) or len(finished_tasks[member_num])%5==0:
            recalc_member_skill_random(member_num, finished_tasks[member_num])

START = time.time()
# 事前情報
N,M,K,R = list(map(int, input().split()))
INI_MEMBER_SKILL = 1
NUM_RANDOM_LOOP = 200
CAND_NUM = 5
TIME_LIMIT = 2.75
task_diff = []
task_diff_order = []
for i in range(N):
    diff = list(map(int, input().split()))
    task_diff.append(diff)

task_depend_in = [[] for _ in range(N)]
task_depend_out = [[] for _ in range(N)]
for i in range(R):
    u,v = list(map(int, input().split()))
    u,v = u-1,v-1
    task_depend_in[v].append(u)
    task_depend_out[u].append(v)

# タスクの依存関係の連鎖が長いものはcritical_taskとする
critical_tasks = []
for i in range(N):
    queue = deque()
    queue.append(i)
    dist = [-1]*N
    dist[i] = 0
    while queue:
        s = queue.popleft()
        for to in task_depend_out[s]:
            if dist[to] != -1:
                continue
            dist[to] = dist[s] + 1
            queue.append(to)
    if max(dist) > 1:
        critical_tasks.append(i)

priority_tasks = critical_tasks + [i for i in range(N) if i not in critical_tasks]

member_skill = [[INI_MEMBER_SKILL] * K for _ in range(M)]
task_start_and_estimate = [[0,1]]*M

finished_tasks = [[] for _ in range(M)]
task_status = [-1]*N # -1: not started 0: started 1: completed
member_status = [-1]*M # -1: not assigned k: assigned task k (0 <= k <= N-1)
max_duration, min_duration = 1, 10**18

day = 0
while True:
    day += 1

    # どのメンバーをどのタスクにアサインするか決定
    assign_list = []
    if member_status.count(-1) != 0:
        assign_list = assign_member_to_task()

    # 出力
    print(len(assign_list), " ".join(assign_list), flush=True)

    # sの予測スキルの出力
    for i in range(M):
        print("#s", i+1, " ".join([str(int(j)) for j in member_skill[i]]))

    # 入力
    feedback = list(map(int, input().split()))
    if feedback[0] == -1:
        print(-1)
        exit()
    else:
        if feedback[0] != 0:
            # タスク完了に要した期間からメンバーのスキルを再見積
            update_status(feedback[1:])