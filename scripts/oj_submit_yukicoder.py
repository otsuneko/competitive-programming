import os,sys
import subprocess
from urllib.request import urlopen

def get_contest_id():
    #実行ファイルがコンテストごとのフォルダか単体ファイルか判定する
    script_path = sys.argv[0]
    file_path = sys.argv[1]
    
    basedir_name = ''

    for i,char in enumerate(file_path):
        if script_path[i].lower() == file_path[i].lower():
            continue
        else:
            basedir_path = file_path[:i]
            file_path = file_path[i:]
            break
    
    #folder形式かfile単体か
    fs = file_path.split('\\')
    idx = fs.index("yukicoder")
    fs = fs[idx:]
    if len(fs)==2:
        parts = fs[-1].split('_')
        problem_id = parts.pop(-1).split('.')[0]
        contest_id = fs[-2]
    if len(fs)==3:
        contest_id = fs[-2]
        problem_id = fs[-1].split('.')[0]

    return basedir_name,contest_id,problem_id

def oj_submit(contest_id,problem_id):
    #check url
    oj_url = "https://yukicoder.me/problems/no/{0}".format(problem_id)
    try:
        f = urlopen(oj_url)
    except:
        print('\n\nURL not found:',oj_url)
        oj_url = input('Please enter contest_url:')

    cp = subprocess.run(['oj','submit','--wait=0','--yes','--no-guess','--language',"pypy3",oj_url,sys.argv[1]])
    if cp.returncode!=0:
        print('oj test failed. exit')
        sys.exit(1)

    return

def main():
    basedir_name,contest_id,problem_id = get_contest_id()

    tmp_path = '{}tmp\\{}_{}'.format(basedir_name,contest_id,problem_id)
    oj_submit(contest_id,problem_id)

if __name__=='__main__':
    main()