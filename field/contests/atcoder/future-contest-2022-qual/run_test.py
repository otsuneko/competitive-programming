import subprocess
import os
import time

# 単発テスト用
# pypy3 "D:\ToBeSaved\TKI13 Documents\GitHub\competitive-programming\field\contests\atcoder\rcl-contest-2021-long\a.py" < "D:\ToBeSaved\TKI13 Documents\GitHub\competitive-programming\field\contests\atcoder\rcl-contest-2021-long\tester\in\input_0.txt"
# pypy3 "D:\ToBeSaved\TKI13 Documents\GitHub\competitive-programming\field\contests\atcoder\rcl-contest-2021-long\a.py" < "D:\ToBeSaved\TKI13 Documents\GitHub\competitive-programming\field\contests\atcoder\rcl-contest-2021-long\tester\in\input_0.txt" > "D:\ToBeSaved\TKI13 Documents\GitHub\competitive-programming\field\contests\atcoder\rcl-contest-2021-long\tester\out\output_0.txt"
# pypy3 "D:\ToBeSaved\TKI13 Documents\GitHub\competitive-programming\field\contests\atcoder\rcl-contest-2021-long\a.py" < "D:\ToBeSaved\TKI13 Documents\GitHub\competitive-programming\field\contests\atcoder\rcl-contest-2021-long\tester\in\input_23.txt" > "D:\ToBeSaved\TKI13 Documents\GitHub\competitive-programming\field\contests\atcoder\rcl-contest-2021-long\tester\out\output_23.txt"

path = "D:\\ToBeSaved\\TKI13 Documents\\GitHub\\competitive-programming\\field\contests\\atcoder\\rcl-contest-2021-long"
score_path = "{0}\\tester\\score.txt".format(path)

# 過去のscoreファイルがあれば削除
if os.path.exists(score_path):
    os.remove(score_path)

# ピックアップ
pick_up = [0,8,11,25,28]
for i in range(50):
# for i in pick_up:
    start = time.time()
    # テスト実行
    cmd = 'pypy3 "{0}\\a.py" < "{0}\\tester\\in\\input_{1}.txt" > "{0}\\tester\\out\\out_{1}.txt"'.format(path,i)
    returncode = subprocess.run(cmd, shell=True, stdout = subprocess.PIPE)
    end = time.time()
    print(end-start)

    # score集計
    cmd = 'pypy3 "{0}\\tester\\judge.py" "{0}\\tester\\in\\input_{1}.txt" "{0}\\tester\\out\\out_{1}.txt" >> "{2}"'.format(path,i,score_path)
    returncode = subprocess.run(cmd, shell=True, stdout = subprocess.PIPE)
