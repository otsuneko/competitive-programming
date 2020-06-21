# 説明

このフォルダはatcoder用のvscode+docker+git環境を構築する自分用のオレオレ環境構築メモです。  
目指せ水色コーダー。  

以下の３つがメインとなっています。 

    1.dockerコンテナの構築  
    2.online-judge-toolsの実行  
    3.グラフ問題の入力可視化  

## フォルダ構成

atcoder  
├── README.md      
├── .devcontainerdocker   
│   ├── devcontainer.json    
│   └── Dockerfile   
├── requirements.txt   
├── version_check.py  
│          
├── .vscode                                       
│   ├── launch.json    
│   ├── task.json    
│   └── py_atcoder_snippet.code-snippets   
│    
├── field  
│   ├── contests  
│   │   └── past1         
│   │       └── a.py  
│   │         
│   └── other_problems     
│       └── abc023_b.py  
│  
├── library  
│   ├── __init__.py  
│   ├── calc_comb.py  
│   └── factorization.py  
│      
├── scripts                                      
│   ├── clean_tmp.sh   
│   ├── graph_show.py  
│   └── oj_test.sh  
│      
└── tmp  


- **.devcontainerdocker** : dokcerコンテナ構築用
- **requirements.txt** : dokcer構築の際にpip installする一覧。atcoderの環境+jupyter,matplotlib,online-judge-toolsを導入
- **version_check.py** : atcoderの環境確認用
- **.vscode** : スニペット一覧やデバッカー、タスクランナーの設定など
- **field** : 問題の解法ファイル
- **library** : コピペ用のライブラリ一覧
- **scripts** : グラフ可視化とonline-judge-toolsの実行ファイル
- **tmp** : online-judge-toolsでダウンロードした入力サンプルの保存場所


## 説明

1. dockerコンテナビルド関連

    .devcontainerにあるdevcontainer.json,Dockerfile、とrequirements.txtでイメージの立ち上げを行っています。

    atocderのジャッジ(2020/6/21時点)でのpython3.8とそのモジュール、他にはグラフ問題の可視化用にjupyter,matplotlib、あとはonline-judge-toolsを導入しています  

2. .vscode
    - launch.json  

        vscodeでのpythonデバッグ設定です。  

    - task.json

        vscodeの`Tasks:Run Build Task`を使用して、oj_test.shを動かすものです。  
        解法ファイル(e.g.abc168_a.py)を開いた状態で、Ctr+Shift+Bで実行可能です。私の環境では。  

        実行されると、online-judge-toolsを用いてファイル名からサンプルをダウンロード、出力のテストまで行われます。
        ![gif](/workspaces/atcoder/sample/sample2.gif)    

    - py_atcoder_snippet.code-snippets  

        vscodeのスニペット一覧です。   

3. field  
    コンテストの解法ファイルをまとめて入れています。contestsでは開催中コンテスト、other_problemsではその他の問題を放り込んでいます。  

    .gitignoreにcontestsを記載することで、PASTの問題などで事故らないようにする想定です。  

4. library  
    典型的なライブラリをコピペ用に入れていく予定のフォルダです  

5. scripts
    - oj_test.sh  

        online-judge-toolsで開いている問題のファイル名からサンプルをダウンロード、出力のテストまで行います。  

    - graph_show.py  

        グラフ問題での入力をnetworkx+jupyterで可視化しようと試みています。いまいちパッとしない。

        tmp以下の指定のフォルダにある入力サンプルをnetworkx+matplotlib+jupyterで可視化します。  

        もしくは入力をブランクにすると、graph_sampleにあるサンプルを実行するのでそこを手入力で直して実行します。  
        ![gif](/workspaces/atcoder/sample/sample.gif)  
        
        入力ファイル形式は↓のようなものを想定  
        #-input.in--  
        #n m  
        #a1 b1  
        #a2 b2  
        #------------  
        

    - clean_tmp.sh  

        oj_test.shを実行するとtmp以下にサンプルがどんどんたまっていくので、その掃除用です。  
        実行すると1日以上前のフォルダを削除します  

