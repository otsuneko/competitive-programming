from re import sub
import subprocess
import time
import sys
import os
from math import log10

# Rustのtester出力からスコア情報を抽出し保存するためのファイル
score_file_path = os.getcwd() + '/../score.txt'
f = open(score_file_path, 'w')

# Rustのtester出力からスコア情報を抽出し保存するためのファイル
score_log_file_path = os.getcwd() + '/../score_log.txt'
f2 = open(score_log_file_path, 'w')

# コマンドライン引数が与えられなければエラー
if len(sys.argv) < 2 or not sys.argv[1].isdecimal():
    print("実行するテストケースの数を入力してください")
    exit()

start_test_case = int(sys.argv[1])
end_test_case = int(sys.argv[2]) if len(sys.argv) > 2 else start_test_case+1
num_test_cases = end_test_case - start_test_case

# Rustのtester出力からスコア情報を抽出し書き出し
total_score = 0
total_score_log = 0
for i in range(start_test_case, end_test_case):
# for i in li_tle:
    start = time.time()
    print("{0}.txt".format(str(i).zfill(4)))
    os.chdir("..")
    # cmd = "cargo run -r --bin tester pypy3 a.py < ./tools/in/{0}.txt > ./tools/out/{0}.txt".format(str(i).zfill(4))
    cmd = "./tools/tester.exe py a.py < ./tools/in/{0}.txt > ./tools/out/{0}.txt".format(str(i).zfill(4))
    # cmd = "pypy3 a.py < ./tools/in/{0}.txt > ./tools/out/{0}.txt".format(str(i).zfill(4))
    returncode = subprocess.run(cmd, shell=True, capture_output=True,text=True)
    print(returncode.stderr, end="")

    os.chdir("./tools")

    cmd = "./vis.exe in/{0}.txt out/{0}.txt".format(str(i).zfill(4))
    # cmd = "cargo run -r --bin vis in/{0}.txt out/{0}.txt".format(str(i).zfill(4))
    returncode = subprocess.run(cmd, shell=True, capture_output=True,text=True)
    end = time.time()
    print(returncode.stdout, end="")

    # 標準出力を改行文字で分割して、各行をリストに格納
    stdout_lines = returncode.stdout.split('\n')

    # ★★★★★ここを問題に応じて書き換える★★★★★
    target_string = "Score = "

    # 特定の文字列を含む行を抜き出す
    matching_lines = [line for line in stdout_lines if target_string in line]

    if matching_lines:
        for line in matching_lines:
            score = line.replace(target_string, "")
            f.write(score)
            f.write("\n")

            score_log = log10(int(score)) if int(score) > 0 else 0
            f2.write(str(score_log))
            f2.write("\n")

            total_score += int(score)
            total_score_log += score_log

    print("Duration time:", end-start)
    print()

f.write(str(total_score))
print("total_score:", total_score)
f.close()

f2.write(str(total_score_log/num_test_cases))
print("avarage_score_log:", total_score_log/num_test_cases)
f2.close()
