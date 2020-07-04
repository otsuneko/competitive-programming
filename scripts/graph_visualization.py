import os,sys,glob
import subprocess
from subprocess import PIPE
from urllib.request import urlopen
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

class Input(object):
    def __init__(self,file_name):
        self.file_name = file_name
        self._inputs = []
        self._path = str(os.path.dirname(__file__)).replace('scripts','')+'tmp/sample'

    def select_graph_type(self):
        ##
        st.title('Atcoder Graph Simulator')
        st.write('Atcoderのグラフ問題に対して、入力サンプルからグラフを可視化します。')
        st.write('サイドバーからグラフ描画のパラメータを変更することができます。')

        ##
        st.header('__1.Selcet a Graph Type__')
        st.write('問題に対応したグラフのタイプを選択してください。以下の形式が選択可能です')
        st.write('(0 or 1index/無向グラフ or 有効グラフ/重みなし or 重みあり/入力形式が隣接リスト or 隣接行列)')

        self._s1 = st.selectbox('0 or 1-indexed',('0-indexed','1-indexed'))
        self._s2 = st.selectbox('non-directed or directed',('non-directed','directed'))
        self._s3 = st.selectbox('non-weighted or weighted',('non-weighted','weighted'))
        self._s4 = st.selectbox('normal or martrix',('normal','martrix'))

        st.write('expected format:')
        if (self._s2=='non-directed' or self._s2=='directed')  and self._s3=='non-weighted' and self._s4=='normal':
            st.latex(r'''
            \begin{array}{cc}
            n& m \\
            a_{1}& b_{1} \\
            \vdots\\
            a_{i}& b_{i} \\
            \end{array}
            ''')

        if (self._s2=='non-directed' or self._s2=='directed')  and self._s3=='weighted' and self._s4=='normal':
            st.latex(r'''
            \begin{array}{ccc}
            n& m \\
            a_{1}& b_{1} & c_{1} \\
            \vdots\\
            a_{i}& b_{i} & c_{i} \\
            \end{array}
            ''')

        if self._s4=='martrix':
            st.latex(r'''
            \begin{array}{ccc}
            n\\
            a_{1,1}& \ldots & a_{1,n}\\
            \vdots\\
            a_{n,1}& \ldots & a_{n,n}\\
            \end{array}
            ''')

    def get_contest_id(self):
        #実行ファイルがコンテストごとのフォルダか単体ファイルか判定する
        script_path = sys.argv[0]
        file_path = sys.argv[1]
        
        basedir_path = ''

        for i,char in enumerate(file_path):
            if script_path[i]==file_path[i]:
                continue
            else:
                basedir_path = file_path[:i]
                file_path = file_path[i:]
                break
        print('filepath:',file_path)
        #folder形式かfile単体か
        fs = file_path.split('/')
        if len(fs)==3:
            parts = fs[-1].split('_')
            problem_id = parts.pop(-1).split('.')[0]
            contest_id = '_'.join(parts)
        if len(fs)==4:
            contest_id = fs[-2]
            problem_id = fs[-1].split('.')[0]

        self._basedir_path = basedir_path
        self._contest_id = contest_id
        self._problem_id = problem_id

    def from_contest(self,types):
        if types=='id':
            st.write('---')
            st.write('problem_idを入力してください(e.g.abc168_d)')
            st.write('※problem_idの問題がtmpフォルダにない場合はダウンロードを実行します')
            
            try:
                problem_id = '{0}_{1}'.format(self._contest_id,self._problem_id)
            except:
                problem_id = ''
            contest_id = st.text_input(label='problem_id',value=problem_id)
        
        if types=='url':
            st.write('---')
            st.write('問題ページのURLを入力してください')
            contest_url = st.text_input(label='contest_URL')
            contest_id = contest_url.split('/')[-1]
        
        inputs = 0
        ###data download
        if contest_id:
            self._tmp_path = str(os.path.dirname(__file__)).replace('scripts','')+'tmp'
            self._path = str(os.path.dirname(__file__)).replace('scripts','')+'tmp/{}'.format(contest_id)

            if st.button('Enter',key=1):
                files = glob.glob('{}/*.in'.format(self._path))
                if not files:
                    m = st.write('not exist.start download...')
                    oj_url="https://atcoder.jp/contests/{}/tasks/{}".format(contest_id.split('_')[0],contest_id)
                    try:
                        f = urlopen(oj_url)
                        os.mkdir(self._path)
                    except:
                        st.write('URL not found:{}'.format(oj_url))
                    
                    subprocess.call('oj d {} --format {}/sample-%i.%e'.format(oj_url,self._path),shell=True)

            #with open files
            inputs = []
            for p in glob.glob('{}/*.in'.format(self._path)):
                with open(p) as input_file:
                    f = [l.strip() for l in input_file.readlines()]
                    inputs.append(f)

            self._inputs = [st.text_area(label='sample{}'.format(i),value='\n'.join(d),key=i) for i,d in enumerate(inputs)]

    def input_data(self):
        st.header('__2.Data Entry__')
        st.write('データの入力オプションを選択することが可能です。')
        st.write('input modeからコンテストid/URL/手入力が選択できます。')

        input_mode = st.selectbox('input mode:',('from problem id','from problem URL','free input'))

        if input_mode=='from problem id':
            self.from_contest('id')
        if input_mode=='from problem URL':
            self.from_contest('url')
        if input_mode=='free input':
            st.write('---')
            inputs = st.text_area(label='free_input').rstrip()
            self._inputs = inputs if inputs else []

        st.write('')
        if self._inputs:
            st.write('Successfully entered the data!')
        else:
            st.write('data not found')


    def draw_option(self):
        st.sidebar.subheader('node option:')
        self._node_size = st.sidebar.slider('node_size:',min_value=100,max_value=3000,step=100,value=800)
        self._node_color = st.sidebar.selectbox('node_color:',('red','coral','gold','green','mediumspringgreen','darkturquoise','blue','darkviolet','white','black'),index=5)
        self._node_shape = st.sidebar.selectbox('node_shape(circle or square):',('o','s'),index=0)
        st.sidebar.subheader('edge option:')
        self._width = st.sidebar.slider('edge_width:',min_value=0.5,max_value=5.0,step=0.5,value=1.0)
        self._edge_color = st.sidebar.selectbox('edge_color:',('red','coral','gold','green','mediumspringgreen','darkturquoise','blue','darkviolet','white','black'),index=9)
        st.sidebar.subheader('other option:')
        self._alpha = st.sidebar.slider('alpha(ノードとエッジの透明度):',min_value=0.0,max_value=1.0,step=0.1,value=0.8)
        self._font_size = st.sidebar.slider('font_size:',min_value=5,max_value=50,step=5,value=15)
        self._font_color = st.sidebar.selectbox('font_color:',('red','coral','gold','green','mediumspringgreen','darkturquoise','blue','darkviolet','white','black'),index=8)
        self._font_weight = st.sidebar.selectbox('font_weight:',('bold','normal'))
        self._k = st.sidebar.slider('k(ノードの反発力):',min_value=0.0,max_value=10.0,step=0.1,value=0.8)
      
    def input(self):
        self.draw_option()
        self.select_graph_type()
        self.get_contest_id()
        self.input_data()

class Draw(Input):
    def __init__(self,file_name):
        super().__init__(file_name)
        super().input()

    def graph_to_networkx(self,idx,data):
        #non-directed,non-weighted,normal
        edge_labels = {}
        if self._s2=='non-directed' and self._s3=='non-weighted' and self._s4=='normal':
            n,m = map(int,data.pop(0).split())
            g = nx.Graph()
            g.add_nodes_from(list(range(idx,n+idx)))
            
            for i in range(m):
                a,b = map(int,data[i].split())
                g.add_edge(a,b)

        ###non-directed,weighted,normal
        if self._s2=='non-directed' and self._s3=='weighted' and self._s4=='normal':
            n,m = map(int,data.pop(0).split())
            g = nx.Graph()
            g.add_nodes_from(list(range(idx,n+idx)))

            for i in range(m):
                a,b,c = map(int,data[i].split())
                g.add_edge(a,b,weight=c)
                edge_labels[(a,b)]=c
        
        ###directed,non-weighted,normal
        if self._s2=='directed' and self._s3=='non-weighted' and self._s4=='normal':
            n,m = map(int,data.pop(0).split())
            g = nx.DiGraph()
            g.add_nodes_from(list(range(idx,n+idx)))
            for i in range(m):
                a,b = map(int,data[i].split())
                g.add_edge(a,b)

        ###directed,weighted,normal
        if self._s2=='directed' and self._s3=='weighted' and self._s4=='normal':
            n,m = map(int,data.pop(0).split())
            g = nx.DiGraph()
            g.add_nodes_from(list(range(idx,n+idx)))
            for i in range(m):
                a,b,c = map(int,data[i].split())
                g.add_edge(a,b,weight=c)
                edge_labels[(a,b)]=c

        ###non-directed,non-weighted,martrix
        if self._s2=='non-directed' and self._s3=='non-weighted' and self._s4=='martrix':
            n = int(data.pop(0))
            data = [list(map(int,d.split())) for d in data]
            g = nx.Graph()
            g.add_nodes_from(list(range(idx,n+idx)))
            for i in range(n):
                for j in range(n):
                    if data[i][j]:
                        g.add_edge(i+idx,j+idx)
        ###non-directed,weighted,martrix
        if self._s2=='non-directed' and self._s3=='weighted' and self._s4=='martrix':
            n = int(data.pop(0))
            data = [list(map(int,d.split())) for d in data]
            g = nx.Graph()
            g.add_nodes_from(list(range(idx,n+idx)))
            for i in range(n):
                for j in range(n):
                    if data[i][j]!=0:
                        g.add_edge(i+idx,j+idx,weight=data[i][j])
                        edge_labels[(i+idx,j+idx)]=data[i][j]
            
        ###directed,non-weighted,martrix
        if self._s2=='directed' and self._s3=='non-weighted' and self._s4=='martrix':
            n = int(data.pop(0))
            data = [list(map(int,d.split())) for d in data]
            g = nx.DiGraph()
            g.add_nodes_from(list(range(idx,n+idx)))
            for i in range(n):
                for j in range(n):
                    if data[i][j]==1:
                        g.add_edge(i+idx,j+idx)

        ###directed,weighted,martrix
        if self._s2=='directed' and self._s3=='weighted' and self._s4=='martrix':
            n = int(data.pop(0))
            data = [list(map(int,d.split())) for d in data]
            g = nx.DiGraph()
            g.add_nodes_from(list(range(idx,n+idx)))
            for i in range(n):
                for j in range(n):
                    if data[i][j]!=0:
                        g.add_edge(i+idx,j+idx,weight=data[i][j])
                        edge_labels[(i+idx,j+idx)]=data[i][j]
        
        fig = plt.figure(figsize=(15,15))
        pos = nx.spring_layout(g,k=self._k)
        nx.draw_networkx(g,pos,
                        node_size=self._node_size,
                        node_color=self._node_color,
                        node_shape=self._node_shape,
                        width=self._width,
                        edge_color=self._edge_color,
                        alpha=self._alpha,
                        font_color=self._font_color,
                        font_weight=self._font_weight,
                        font_size=self._font_size)
        if edge_labels:
            nx.draw_networkx_edge_labels(g,pos,edge_labels=edge_labels,font_size=self._font_size-2)
        plt.axis('off')
        return fig

    def graph_draw(self):
        idx = 0 if self._s1=='0-indexed' else 1
        inputs = [d.split('\n') for d in self._inputs]
        st.header('__3.Graph Draw__')
        st.write('Graph Drawボタンでグラフを描画します。')
        st.write('- save picのチェックボックスをつけると、tmp/graph_sample/に画像が保存されます。')
        st.write('- データの入力形式がexpected formatと異なる場合には適宜変更してください。')
        save_button = st.checkbox('save pic',key=44)
        draw_button = st.button('Graph Draw',key=33)
        images = []
        if draw_button:
            try:
                for i,data in enumerate(inputs):
                    image = self.graph_to_networkx(idx,data)
                
                    images.append(image)
                    st.write('---')
                    st.write('sample{}_graph'.format(i))
                    st.write(image)
            except:
                st.write('draw error')
        else:
            st.write('no image')

        
        if save_button:
            for i,pic in enumerate(images):
                pic.savefig('{}/graph_sample/sample{}.png'.format(self._tmp_path,i))
    
def main():
    Draw(sys.argv[-1]).graph_draw()
    print('\n')
    print('please acsess:')
    print('http://localhost:8501')

if __name__=='__main__':
    main()