import os
import subprocess
import datetime
BASH = '/bin/bash'

date = str(datetime.datetime.now()).replace(" ","_")
for i in range(1,2):
    # テスト実行
    cmd = 'cargo run --release --bin rco-contest-2019-qual-b < ./testcases/b/in/input_{0}.txt > ./testcases/b/out/output_{0}.txt'.format(str(i))
    returncode = subprocess.run(cmd, shell=True, stdout = subprocess.PIPE, executable=BASH)

    # スコア集計
    cmd = 'python3 judge.py ./testcases/b/in/input_{0}.txt ./testcases/b/out/output_{0}.txt >> score_{1}.txt'.format(str(i), date)
    returncode = subprocess.run(cmd, shell=True, stdout = subprocess.PIPE, executable=BASH)