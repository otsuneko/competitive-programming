import os,sys
import subprocess

def main():
    file_path = sys.argv[1]
    fs = file_path.split('\\')

    # oj-prepareで事前に作成したフォルダのパス
    file_path2 = "\\".join(fs[:-1]) + "\\" + fs[-2] + "_" + fs[-1].split(".")[0]
    print(file_path2)

    if not os.path.exists(file_path2):
        print("folder does not exist.")
        exit()
    
    # random test
    cp = subprocess.run(['oj','g/i','python generate.py','10'], cwd=file_path2)
    if cp.returncode!=0:
        print('generate random case failed. exit')
        sys.exit(1)

    cp = subprocess.run(['oj','g/o','-c','python ..\\{}'.format(fs[-1])], cwd=file_path2)
    if cp.returncode!=0:
        print('random test failed. exit')
        sys.exit(1)

if __name__=='__main__':
    main()