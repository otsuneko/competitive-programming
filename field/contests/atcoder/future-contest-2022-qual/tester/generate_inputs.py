import subprocess
import os

path = "D:\\ToBeSaved\\TKI13 Documents\\GitHub\\competitive-programming\\field\contests\\atcoder\\rcl-contest-2021-long\\tester"

for i in range(30,50):

    # テストケース生成
    cmd = 'python "{0}\\generator.py" {1} > "{0}\\in\\input_{1}.txt"'.format(path,i)
    returncode = subprocess.run(cmd, shell=True, stdout = subprocess.PIPE)
