# 説明

このフォルダはatcoder用のvscode+docker+git環境を構築する自分用のオレオレ環境構築メモです。  
pythonとc++で実行可能です。

以下の３つがメインとなっています。 

    1.dockerコンテナの構築設定周り  
    2.online-judge-toolsの実行  
    3.グラフ問題の入力可視化  

## フォルダ構成
atcoder_docker_sample   
│        
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
│      
├── scripts                                      
│   ├── clean_tmp.sh   
│   ├── graph_visualization.py  
│   ├── oj_test.py  
│   └── oj_submit.py  
│      
└── tmp  


- **.devcontainerdocker** : dokcerコンテナ構築用
- **requirements.txt** : dokcer構築の際にpip installする一覧。atcoderの環境,matplotlib,online-judge-tools,streamlitを導入
- **version_check.py** : atcoderの環境確認用
- **.vscode** : スニペット一覧やデバッカー、タスクランナーの設定など
- **field** : 問題の解法ファイル
- **library** : コピペ用のライブラリ一覧
- **scripts** : グラフ可視化とonline-judge-toolsの実行ファイル
- **tmp** : online-judge-toolsでダウンロードした入力サンプルの保存場所

## 導入

簡単な導入＆立ち上げ方法です。わかる人はスキップ推奨

0. __前準備__

    vscode+dockerが動かせる環境が必要です。
    導入については下記参照：
    https://code.visualstudio.com/docs/remote/containers
    https://code.visualstudio.com/blogs/2020/03/02/docker-in-wsl2

1. __gitからのダウンロード__   

    githubからのダウンロード方法です。
    ```
    git clone https://github.com/yamatia/atcoder_docker_sample.git
    ```

2. __VSCodeで開く__

    左下の`><`マークをクリックして、`Remote Containers:Open Foleder in Container`から1でダウンロードしたatcoder-docker-samleをクリックする  
    
    ![docker](https://raw.github.com/wiki/yamatia/atcoder_docker_sample/image/docker.gif)
    
    初回は少し時間がかかりますが、dockerイメージがビルドされて実行可能になります。  
    ※docker imageのサイズが大きいですが、不満な人はdevcontainer.jsonからextensionを適宜削除してください 

3. __atcoderへのログイン__  
    online-judge-toolsでの提出を行うのであればログイン作業が必要です。
    以下を入力するとユーザー名とパスワードを求められるので適宜入力してください。

    ```
    oj login https://atcoder.jp/
    ```

## 使い方

- コンテストの解法はfield以下に収める事を想定してます。/field/contest/abc168/d.pyのようにフォルダで管理するか、/field/other_problems/abc168_d.pyのように問題で管理することができます。<br><br>
.gitignoreには/field/contestsを記載しているので、この部分はGitしても上がりません。なのでPASTの問題などをここで管理して賠償問題事故などをおこさないようにしています。

- 基本的に、解法ファイルを作成する以外の操作はすべてタスクランナーでGUIから実行可能です。解法ファイルを開いた状態で、左下のTASK RUNNNERから以下の５つを選択することで操作できます。<br><br>

    1. __oj_download&test__   

        online-judge-toolsのdownloadとtestをいい感じに実行するようにしています。    
        フォルダ名とファイル名から、atcoderの問題URLにアクセスし、tmp以下に問題ファイルをダウンロード、実行テストという作業をまとめて行っています。     
        ※企業コンなどで時に問題URLに辿り着けないことがあるので、その時はterminalから入力を求められます。

        ![oj_download](https://raw.github.com/wiki/yamatia/atcoder_docker_sample/image/oj_download_test.gif)

    2. __oj_submit__    
    
        online-judge-toolsのsubmitを実行するようにしてます。これでatcoderへの提出が行えます。
        
        ![oj_test](https://raw.github.com/wiki/yamatia/atcoder_docker_sample/image/oj_submit.gif)

        ※1つ注意点として、そのままだと実行時にoj側から最後にエラーメッセージが表示されます。しかしコンテストページを見るとわかるのですが、提出はできています。
        これは、online-judge-toolsの挙動として、ファイル提出後にブラウザで提出画面を自動で開こうとするのですが、dockerからホストのブラウザが参照できないことが原因です。提出後にブラウザで開いてほしい人は適宜パスを追加すればいいと思います。

    3. __clean tmp folder__ 
           
        上記1を実行すると、tmp以下にsampleファイルがたまっていくので、その掃除用です。実行すると、1日以上前にダウンロードしたファイルを削除します。

    4. __cpp runner__     
      
        C++の実行ファイル(.cpp形式)をコンパイル、実行します。入力はterminalから行ってください。

    5. __graph viewer__   

        streamlitによるグラフ問題の簡易な可視化用です。<br><br>
        実行すると、<https://localhost:8501/>でブラウザからアクセスできます。<br>

        ![graph](https://raw.github.com/wiki/yamatia/atcoder_docker_sample/image/graph.gif)
        
        基本的に上からポチポチ操作すれば、対応してるグラフ形式であればnetworkxによる可視化が可能です。他には、サイドバーからグラフの描画設定をいじることができます。一応保存も可能です。

        終わったらCtr+Cなどで閉じてあげてください。

- 他には、pythonとc++についてはF5でvscodeのデバッグを実行できます。c++についてはエラーメッセージが流れることもあり少し微妙です。

## その他説明

1. __dockerコンテナビルド関連__

    .devcontainerにあるdevcontainer.json,Dockerfile、とrequirements.txtでイメージの立ち上げを行っています。

    atocderのジャッジ(2020/6/21時点)でのpython3.8とそのモジュール、他にはグラフ問題の可視化用にjupyter,matplotlib、あとはonline-judge-toolsを導入しています。あとC++(GCC)も

    dockerのイメージをコピペしていじりたい人はこの3つだけコピーして環境構築すれば楽だと思います。  

2. __.vscode__
    - launch.json  

        vscodeでのpythonデバッグ設定です。python,c++で実行可能です。
        ※c++は仕様上、step overでプログラムで末端まで走らせるとエラーメッセージ出ます 

    - task.json

        vscodeの`Tasks:Run Build Task`を使用して、いろいろ動かす設定をしてます。  
        解法ファイル(e.g.abc168_a.py)を開いた状態で、Ctr+Shift+Bでデフォルトのビルドタスクを実行可能です。     

    - py_atcoder_snippet.code-snippets  

        vscodeのスニペットです。現状pythonの入力回りだけ設定してます。適宜追加すればより便利に。 

3. __field__  
    コンテストの解法ファイルをまとめて入れています。contestsでは開催中コンテスト、other_problemsではその他の問題を放り込んでいます。  

    .gitignoreにcontestsを記載することで、PASTの問題などで事故らないようにする想定です。  

4. __library__  
    典型的なライブラリをコピペ用に入れていく予定のフォルダです  

5. __scripts__  
    タスクランナーで動かす用のファイルをおいています。

6. __requirements.txt__     
    docker立ち上げ時にpip installするモジュールのリストです

7. __version_check.py__     
    AtCoderのコードテストで実行することで、ジャッジに導入されているモジュールのバージョンを確認することができます。




        

