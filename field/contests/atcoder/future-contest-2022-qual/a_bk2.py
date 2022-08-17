import sys
input = lambda: sys.stdin.readline().rstrip()
import time
import random
import math
#依存関係にあるタスクが完了されているか
def if_depend_task_finished(task):
    res = True
    for necessary in task_depend_in[task]:
        if task_status[necessary] != 1:
            res = False
            break
    return res

# タスクへのアサインリストを乱数で複数パターン用意して一番ギャップが少ないものを採用
def assign_member_to_task_rand():
    NOW = time.time()
    loop_num = 1 if day == 1 or (NOW-START) > TIME_LIMIT else member_status.count(-1)**2
    assign_lists = []
    for loop in range(loop_num):
        tmp_task_status = [*task_status]
        tmp_member_status = [*member_status]
        assign_list = []
        total_skill_gap = 0
        # for task_num in range(N):
        for task_num in priority_tasks:
            if tmp_task_status[task_num] != -1 or not if_depend_task_finished(task_num):
                continue
            cand_members = []
            for skill,member_num,_ in member_skill:
                if tmp_member_status[member_num] != -1:
                    continue
                if day != 1 and len(cand_members) > 2:
                    break
                cand_members.append([member_num,0]) # [メンバーID、要求スキルとの差(w)]
                for k in range(K):
                    skill_gap = task_diff[task_num][k] - skill[k]
                    cand_members[-1][1] += max(0,skill_gap)
        
            # 全メンバーが何らかのタスクを持っている場合は終了
            if member_status.count(-1) == 0:
                break

            if len(cand_members) > 0:
                # 1周目はギャップが最も少ないアサインを、2周目からはランダムな組み合わせ
                r = random.randint(0,min(1,len(cand_members)-1)) if loop != 0 else 0
                cand_members.sort(key=lambda x:(x[1]))
                total_skill_gap += cand_members[r][1]
                tmp_member_status[cand_members[r][0]] = task_num
                tmp_task_status[task_num] = 0
                assign_list.append([cand_members[r][0], task_num, cand_members[r][1]])

        assign_lists.append([total_skill_gap, assign_list])

    # 最終的なアサインの選定
    assign_lists.sort()
    final_choice = []
    if len(assign_lists) > 1:
        r = random.random()
        # prob = max(1,assign_lists[0][0])/max(1,assign_lists[1][0])
        final_choice = [*assign_lists[0][1]] if r < 0.5 else [*assign_lists[1][1]]
    elif len(assign_lists) > 0:
        final_choice = [*assign_lists[0][1]]

    assign_list = []
    for member_num, task_num, estimated_dur in final_choice:
        member_status[member_num] = task_num
        task_status[task_num] = 0
        task_start_and_estimate[member_num] = [day, max(1, estimated_dur)]
        assign_list.append(str(member_num+1) + " " + str(task_num+1))

    return assign_list

# あるメンバーの推定スキルを基に計算した工数がどれだけ過去の実所要時間からズレているか計算
def calc_skill_gap(fin_tasks, member_skill):
    gap = 0
    skip_cnt = 0
    for task_num, duration in fin_tasks:
        w = 0
        for k in range(K):
            w += max(0, task_diff[task_num][k] - member_skill[k])
        w = 1 if w == 0 else w
        # 所要時間が1かつw=0の時は、各diffとskillの差が不明確なのでスキップ
        if duration == 1 and w == 0:
            skip_cnt += 1
            continue
        gap += abs(duration - w)**2
    # MAE → NRMSDに変更
    gap = math.sqrt(gap/(len(fin_tasks)-skip_cnt)) / (max(1,(max(y) - min(y))))
    return gap

# これまでにあるメンバーが遂行した各タスクの実所要時間を基に
# スキルを乱数でブレさせて、最も実績にフィットするスキルを探索
def recalc_member_skill_random(member, fin_tasks):

    # 現在の推定スキルがどれだけ過去の実績からズレているか計算
    idx = 0
    for i in range(M):
        if member_skill[i][1] == member:
            idx = i
            break
    ini_gap = calc_skill_gap(fin_tasks, member_skill[idx][0])
    # print("#ini_gap:",ini_gap)

    # print("#member_skill_before:",member_skill[member])
    best_fit_skills = [[ini_gap, [*member_skill[idx][0]]] for _ in range(CAND_NUM)] # [gap, skills]

    # NUM_RANDOM_LOOP回乱択する
    for _ in range(NUM_RANDOM_LOOP):
        # ブレさせたスキルを生成
        member_skill_rand = [[0]*K for _ in range(CAND_NUM)]
        for i in range(CAND_NUM):
            for k in range(K):
                member_skill_rand[i][k] = max(0,best_fit_skills[i][1][k] + random.randint(-1,1))

            # 生成したスキルがどれだけ過去の実績にフィットしているか検証
            gap = calc_skill_gap(fin_tasks, member_skill_rand[i])
            # print("#gap:",gap)

            # 過去の実所要時間とのギャップがより少なければ採用
            # if gap < best_fit_skills[i][0]:
            if gap < best_fit_skills[i][0]:
                best_fit_skills[i][0] = gap
                best_fit_skills[i][1] = [*member_skill_rand[i]]

    best_fit_skills.sort()
    # print("#best_fit_skills:",best_fit_skills)
    member_skill[idx][0] = [*best_fit_skills[0][1]]
    member_skill[idx][2] = sum(member_skill[idx][0])
    # print("#member_skill_after:",member_skill[member])

# 各種ステータスの更新
def update_status(finish_members):
    global beginners
    for member_num in finish_members:
        member_num -= 1 # 0-index
        task_num = member_status[member_num]
        task_status[task_num] = 1
        member_status[member_num] = -1
        duration, estimated_duration = day - task_start_and_estimate[member_num][0] + 1, task_start_and_estimate[member_num][1]
        y.append(duration)
        finished_tasks[member_num].append((task_num, duration))

        # M個のタスクをこなしたメンバーをリストに追加していき、最後に残った3人はスキルの低いメンバーとする
        if len(finished_tasks[member_num]) == M:
            member_finish_M.add(member_num)
        if len(beginners) == 0 and len(member_finish_M) >= M - NUM_BEGINNERS:
            beginners = set([i for i in range(M)]) - member_finish_M
            # print("#beginners:",beginners)

        # あるメンバーがこなしたタスクが一定回数になったら、過去の実績を基にスキルを乱択調整
        finish_task_num = len(finished_tasks[member_num])
        NOW = time.time()
        if (NOW-START) > TIME_LIMIT:
            continue
        if (finish_task_num < M and finish_task_num%2) or len(finished_tasks[member_num])%10==0:
            recalc_member_skill_random(member_num, finished_tasks[member_num])
            # メンバーをスキル順にソート
            member_skill.sort(key=lambda x:x[2], reverse=True)

START = time.time()
# 事前情報
N,M,K,R = list(map(int, input().split()))
INI_MEMBER_SKILL = 1
NUM_RANDOM_LOOP = 200
NUM_BEGINNERS = 3
CAND_NUM = 5
TIME_LIMIT = 2.75
task_diff = []
task_diff_order = []
for i in range(N):
    diff = list(map(int, input().split()))
    task_diff.append(diff)
    task_diff_order.append((i,sum(diff)))
task_diff_order.sort(key=lambda x:x[1])
hard_tasks = set([task_num for task_num,_ in task_diff_order[int(N*0.95):]])

task_depend_in = [[] for _ in range(N)]
critical_tasks = set()
for i in range(R):
    u,v = list(map(int, input().split()))
    u,v = u-1,v-1
    task_depend_in[v].append(u)
    if v-u < 5:
        critical_tasks.add(u)

hard_critical_tasks = hard_tasks or critical_tasks
# priority_tasks = list(hard_critical_tasks) + [i for i in range(N) if i not in hard_critical_tasks]
priority_tasks = []
for i in range(N):
    if i%50 == 0:
        for task_num in hard_critical_tasks:
            if i <= task_num < i+50:
                priority_tasks.append(task_num)
    if i not in hard_critical_tasks:
        priority_tasks.append(i)

# print("#task_diff_order:",task_diff_order)
# print("#hard_critical_tasks:",hard_critical_tasks)

member_skill = [[[INI_MEMBER_SKILL]*K, i, INI_MEMBER_SKILL*K] for i in range(M)]
member_skill_order = []
beginners = set()
member_finish_M = set()
task_start_and_estimate = [[0,1]]*M

finished_tasks = [[] for _ in range(M)]
task_status = [-1]*N # -1: not started 0: started 1: completed
member_status = [-1]*M # -1: not assigned k: assigned task k (0 <= k <= N-1)
y = [1]

day = 0
while True:
    day += 1

    # どのメンバーをどのタスクにアサインするか決定
    assign_list = []
    if member_status.count(-1) != 0:
        assign_list = assign_member_to_task_rand()

    # 出力
    # print("#",assign_list)
    print(len(assign_list), " ".join(assign_list), flush=True)
    # print("#",task_status)
    # print("#member_status:",member_status)
    # print("#task_start_and_estimate:",task_start_and_estimate)

    # sの予測スキルの出力
    # member_skill.sort(key=lambda x:x[2],reverse=True)
    # for skill,member_num,_ in member_skill:
    #     print("#s", member_num+1, " ".join([str(k) for k in skill]))

    # 入力
    feedback = list(map(int, input().split()))
    if feedback[0] == -1:
        print(-1)
        exit()
    else:
        if feedback[0] != 0:
            # タスク完了に要した期間からメンバーのスキルを再見積
            # print("#finished_tasks:",*[(i+1,len(tasks)) for i,tasks in enumerate(finished_tasks)])
            update_status(feedback[1:])