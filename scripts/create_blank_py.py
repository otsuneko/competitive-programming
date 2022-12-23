import os,sys

#コンテスト種別(AtCoder、Codeforces)に応じて、今いるコンテストフォルダ配下に回答用の空pythonファイルを作成する
def main():
    #コンテスト種別の判定
    script_path = sys.argv[0]
    file_path = sys.argv[0]
    print(script_path)
    
    fs = file_path.split('\\')
    print(fs)
    
if __name__=='__main__':
    main()