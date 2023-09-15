#!python

# Parallel processing tester driver for AtCoder Heuristic Contest
# Copyright (c) 2022 toast-uz
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php
#
# USAGE: (eval.py has executable permission)
# 1) Run all tests simultaneously:   ./eval.py
# 2) Run a specified test:           ./eval.py -s test_id    (ex) ./eval.py -s 0
# 3) Run specified tests:            ./eval.py -s test_from test_to   (ex) ./eval.py -s 0 9
# 4) Run with force compile tester:  ./eval.py -f
# 5) Run all tests sequentially:     ./eval.py -seq
#
# Verified by Python3.9.10 & PyPy3.7.12 on MacOS Monterey 12.4

import time
import os
import sys
import subprocess
import argparse
from multiprocessing import Process, SimpleQueue, cpu_count

parent_dir = os.getcwd().split('/')[-1] # 親ディレクトリ: ahc###（###は3桁の数字） を前提とする

# この定数は、通常のAHC開催（Rustでスコアツールvisが提供される）であれば変更不要
tools_dir = './tools/'              # ツールディレクトリ
source_dir = 'src/bin/'             # ソースディレクトリ
rust_target_dir = '/home/otsuneko/workspace/competitive-programming/target/release/'   # Rustのビルド共通ディレクトリ
tester_name = 'vis'                 # テスターのファイル名のsuffix除いた部分
tester_suffix = '.rs'               # テスターのファイル名のsuffix
tester_source = tools_dir + source_dir + tester_name + tester_suffix   # テスターのソースファイル
tester = rust_target_dir + tester_name   # テスターの実行ファイル
input_dir = tools_dir + 'in/'       # テスト入力ファイルディレクトリ
output_dir = tools_dir + 'out/'     # テスト出力ファイルディレクトリ
test_from = 0                       # テストファイル名番号初期値
test_digits = 4                     # テストファイル名のテスト番号の0-paddingの桁数
suffix = '.txt'                     # テストファイル名

# 以下の定数は個々の開催や、利用者の環境によって変更可能性あり
test_num = 50       # テスト回数（50または100が多い、さらにテストケースを増やせばそれに応じて変更可能）
max_workers = 4  # 並列処理の同時最大数、デフォルトNoneの場合はCPUコア数 * 2
testee_name = 'a'   # 提出プログラムのソースファイル名のsuffix除いた部分
timeout = 60        # 提出プログラムのタイムアウト
## 提出プログラムがRustの場合
# testee_suffix = '.rs'   # 提出プログラムのソースファイル名のsuffix
# testee_source = source_dir + testee_name + testee_suffix # 提出プログラムのソースファイル
# testee_target = parent_dir + '-' + testee_name  # 提出プログラムの実行ファイル名
# ↑ cargo competeで作成したCargo.tomlを前提にしているため、ソースとターゲットの名前は異なっています
# testee = rust_target_dir + testee_target # 提出プログラムの実行パス（Rustの場合）
# testee_exec = testee    # 提出プログラムの実行コマンド（Rustの場合）
## 提出プログラムがPyPy3の場合（ソースはプロジェクトルートに配置）
testee_suffix = '.py'
testee_source = testee_name + testee_suffix
testee_target = testee_source
testee = testee_target
testee_exec = 'pypy3 ' + testee

# 以下は変更不要
RED = '\033[1m\033[31m'
BLUE = '\033[1m\033[34m'
GREEN = '\033[1m\033[32m'
MAGENTA = '\033[1m\033[35m'
NORMAL = '\033[0m'
ERROR = f'{RED}Error{NORMAL}: '
WARN = f'{MAGENTA}Warn{NORMAL}: '
argmax = lambda x: max([(x, i) for i, x in enumerate(x)])[-1]
silent = False
def dbg(*arg):
    if not silent: print(*arg)

# テスト実行用の子プロセス
def single_test(i, q=None, silent=False):
    filename = str(i).zfill(test_digits)
    input_filename = input_dir + filename + suffix
    output_filename = output_dir + filename + suffix
    try:
        if not silent: print(f'Run #{i} ...')
        stime = time.time()
        cp = subprocess.run(testee_exec + ' < ' + input_filename + ' > ' + output_filename,
            shell=True, timeout=timeout, stderr=subprocess.PIPE, text=True)
        dtime = time.time() - stime
        if silent: print(f'#{i:04}:{cp.stderr.rstrip()}')
        else: print(f'{BLUE}{cp.stderr.rstrip()}{NORMAL}')
        if not silent: print(f'Finished #{i}, time: {dtime:.3f}ms')
        if q is not None:
            q.put((i, dtime))
    except subprocess.TimeoutExpired:
        dtime = time.time() - stime
        if not silent: print(f'Timeout expired #{i} time: {dtime:.3f}ms')
    return dtime

# 実行中のプロセス数を求める
def num_active(proc_list):
    return sum([elm[0].is_alive() for elm in proc_list if elm is not None])

# コマンドライン引数の解析用
def parser():
    global test_from, test_num
    parser = argparse.ArgumentParser(
        description='Parallel processing tester driver for AtCoder Heuristic Contest')
    parser.add_argument(
        '-s', '--specified', nargs='*', type=int,
        help='Test specified number as [from [to]] .',
        default=[test_from, test_num - test_from - 1])
    parser.add_argument('-f', '--force',
        help='Force (re)build tester.', action='store_true')
    parser.add_argument('--seq',
        help='Force sequential tests.', action='store_true')
    parser.add_argument('--silent',
        help='Silent mode on.', action='store_true')
    args = parser.parse_args()
    if len(args.specified) > 2:
        print(ERROR + 'To many specified test number.')
        exit(1)
    test_from = args.specified[0]
    test_num = args.specified[1] - test_from + 1 if len(args.specified) == 2 else 1
    if test_from < 0:
        print(ERROR + f'Specified illegal test number: {test_from}')
        exit(1)
    if test_num <= 0:
        print(ERROR + f'Specified illegal number of tests: {test_num}')
        exit(1)
    for i in range(test_from, test_from + test_num):
        filename = str(i).zfill(test_digits)
        input_filename = input_dir + filename + suffix
        if not os.path.isfile(input_filename):
            print(ERROR + f'Input file: {input_filename} or others are not found.')
            exit(1)
    return args

# 初期環境確認と設定
def init_environment(force_build=False):
    # toolsディレクトリ、テスターソースが存在しなければ、異常終了する
    if not os.path.isdir(tools_dir):
        print(ERROR +f'Directory: {tools_dir} is not found.'
            ' Download the local tool (Rust), extract, and copy it'
            ' to the current directory (= project root).')
        exit(1)
    if not os.path.isfile(tester_source):
        print(ERROR + 'Tester source file: {tester_source} is not found.')
        exit(1)
    # テスタービルドイメージが存在しないか古ければ、ビルドする
    # （古いかどうかは、toolsディレクトリとビルド済テスターのタイムスタンプを比較して判断
    #   ※以前のAHCのテスターが残存している可能性を考慮）
    if (force_build or not os.path.isfile(tester)
            or os.stat(tools_dir).st_mtime > os.stat(tester).st_mtime):
        if not force_build:
            print(WARN + 'Tester is not compiled or old.')
        print(f'{RED}CLEAN UP{NORMAL} all release build in {rust_target_dir}'
              f' {RED}BEFORE{NORMAL} build tester.')
        if input(f'{RED}Proceed (yes / no) ? {NORMAL}') != 'yes':
            print('Please build tester manually.')
            exit(1)
        os.chdir(tools_dir)
        os.system('cargo clean --release')
        os.system('cargo build --release --bin ' + tester_name)
        os.chdir('../')
        print('If your program made by Rust, probably you have to rebuild it.')
    if not os.path.isfile(testee) or os.stat(testee_source).st_mtime > os.stat(testee).st_mtime:
        print(ERROR + f'Your build file: {testee} is not compiled or old.')
        print(f'{RED}Auto rebuild{NORMAL}')
        res = os.system('rustup run 1.42.0 cargo build --release --bin ' + testee_target)
        if res != 0:
            print(ERROR + f'Your build file cannot be compiled.')
            exit(1)
    if not os.path.isdir(output_dir):
        print(WARN + 'Test output dir has not been created. Make the dir.')
        os.mkdir(output_dir)

# 並列テスト実行部
def parallel_test_all(max_workers):
    # 並列処理の同時最大数の設定
    num_cpu = cpu_count()
    if max_workers is None:
        max_workers = num_cpu * 2   # 並列実行数
    dbg(f'{GREEN}Run max {max_workers} simultaneous tests on {num_cpu} cpu cores.{NORMAL}')
    # 問題を順次読み込んでテストする（並列処理）
    proc_list = [None] * test_num
    q = SimpleQueue()
    for i in range(test_num):
        # 最大起動済なら待つ
        test_id = test_from + i
        dbg(f'Running: {num_active(proc_list)} simultaneous tests.')
        while num_active(proc_list) >= max_workers:
            time.sleep(0.001)
        # テスト対象プログラムを起動する
        proc = Process(target=single_test, args=(test_id, q, silent))
        proc.start()
        proc_list[i] = (proc, test_id)
    # すべて終了するまで待つ
    dbg(f'Running: {num_active(proc_list)} simultaneous tests. Wait to finish.')
    while num_active(proc_list) > 0:
        time.sleep(0.001)
    assert num_active(proc_list) == 0
    dbg(f'{GREEN}All tests finieshed.{NORMAL}')
    # 結果を取り込む
    dtimes = [None] * test_num
    while not q.empty():
        test_id, dtime = q.get()
        dtimes[test_id - test_from] = dtime
    assert all([dtime > 0 for dtime in dtimes])
    # 時間誤差修正のため1つだけテストを実行する（silentの場合は、余計なログになるため実行しない）
    dbg(f'{GREEN}Run one test again to get the time fix rate.{NORMAL}')
    if not silent:
        dtime_fix_rate = single_test(argmax(dtimes), silent=silent) / dtimes[argmax(dtimes)]
    else: dtime_fix_rate = 1
    return dtimes, dtime_fix_rate

# シーケンシャルテスト実行部
def sequential_test_all():
    # コマンドライン引数があれば特定テスト1つを限定実行
    dbg(f'{GREEN}Run sequential test.{NORMAL}')
    dtimes = [None] * test_num
    for i in range(test_num):
        test_id = test_from + i
        # テスト対象プログラムを起動する
        dtimes[i] = single_test(test_id, silent=silent)
    return dtimes, 1

# テスターを使ってスコアを求める
def compute_score(i):
    test_id = test_from + i
    filename = str(test_id).zfill(test_digits)
    input_filename = input_dir + filename + suffix
    output_filename = output_dir + filename + suffix
    proc = subprocess.run(tester + ' ' + input_filename + ' ' + output_filename,
        shell=True, stdout=subprocess.PIPE, text=True)
    # テスター出力からスコアの抽出（テスターによっては書き換え必要）
    try:
        assert proc.stdout.split()[0] == 'Score'
        score = int(proc.stdout.split()[-1])
    except:  # スコア数値が取れない場合、実行エラーメッセージの可能性が高いためそのまま出力
        print(f'#{i}: {RED}{proc.stdout}{NORMAL}')
        score = 0
    return score

def main():
    global test_from, test_num, max_workers, silent
    args = parser()
    force_build = args.force
    force_sequential = args.seq or test_num == 1
    silent = args.silent
    # ディレクトリ確認など前準備
    init_environment(force_build)
    # テスト実行
    total_stime = time.time()
    dtimes, dtime_fix_rate = sequential_test_all() if force_sequential \
                             else parallel_test_all(max_workers)
    total_dtime = time.time() - total_stime
    # テスターに各テスト結果を読み込ませてスコアを求め、表示する
    if silent: exit()
    print(f'{GREEN}All tests finished. Compute scores...{NORMAL}')
    score_sum = 0
    max_dtime = 0
    max_dtime_fixed = 0
    for i in range(test_num):
        score = compute_score(i)
        dtime_fixed = dtimes[i] * dtime_fix_rate
        print(f'#{test_from + i}: score: {score}, time: {dtimes[i]:.3f}s,'
              f' time(fixed): {dtime_fixed:.3f}s')
        score_sum += score
        max_dtime = max(max_dtime, dtimes[i])
        max_dtime_fixed = max(max_dtime_fixed, dtime_fixed)
    print(f'{GREEN}Total_score: {score_sum}, max_time: {max_dtime:.3f}s, max_time(fixed):'
          f' {max_dtime_fixed:.3f}s')
    print(f'Total_time: {total_dtime:.3f}s ({total_dtime / test_num:.3f}s/test)'
          f' -> x{sum(dtimes) / total_dtime:.1f} faster than sequential.{NORMAL}')
    if score_sum == 0:
        print(WARN + 'The tester may be from a different contest.')

if __name__ == '__main__':
    main()