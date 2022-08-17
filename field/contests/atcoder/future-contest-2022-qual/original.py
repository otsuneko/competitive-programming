# assign random tasks to team member 1.
import sys
import random
# Prior information
n, m, d, r = list(map(int, input().split()))
task_difficulty = []
for i in range(n):
    task_difficulty.append(list(map(int, input().split())))
task_dependency = [[] for _ in range(n)]
for i in range(r):
    temp = list(map(int, input().split()))
    task_dependency[temp[1] - 1].append(temp[0] - 1)
# -1: not started
#  0: started
#  1: completed
task_status = [-1] * n
# -1: not assigned
#  k: assigned task k (1 <= k <= N)
member_status = -1
day = 0
while True:
    day += 1
    output = [0]
    # random search for tasks
    if member_status < 0:
        tasklist = list(range(n))
        random.shuffle(tasklist)
        for task in tasklist:
            if task_status[task] != -1:
                continue
            ok = True
            for necessary in task_dependency[task]:
                if task_status[necessary] != 1:
                    # the dependent tasks have not been completed
                    ok = False
                    break
            if ok:
                # assign the task to team member 1
                task_status[task] = 0
                member_status = task
                output = [1, 1, task + 1]
                break
    str_output = map(str, output)
    print(" ".join(str_output))
    # After the output, you have to flush Standard Output
    sys.stdout.flush()
    temp = list(map(int, input().split()))
    if len(temp) == 1:
        if temp[0] == -1:
            # elapsed days == 2000, or all the tasks have been completed
            exit()
        else:
            # no change in state
            pass
    else:
        # one task has been completed
        task = member_status
        task_status[task] = 1
        member_status = -1