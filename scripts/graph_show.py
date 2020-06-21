#%%
import os,glob
import networkx as nx
import matplotlib.pyplot as plt

#-input.in--
#n m
#a1 b1
#a2 b2
#------------
def graph_draw(path):
    with open(path) as input_file:
        f = [l.strip() for l in input_file.readlines()]

    input0,*inputs = map(str,f) 
    n,m = map(int,input0.split())
    print('node={},edge={}'.format(n,m))
    print('edges:\n{}'.format(inputs))

    g = nx.Graph()
    g.add_nodes_from(list(range(1,n+1)))
    for i in range(m):
        a,b = map(int,inputs[i].split())
        g.add_edge(a,b)

    plt.figure(figsize=(15,15))
    pos = nx.spring_layout(g)
    nx.draw_networkx(g,pos,node_color='blue', node_size=800,alpha=0.8,font_color='w',font_weight='bold',font_size=16)

    plt.show()

def main():
    input_path = input('enter:folder_name of tmp /or None')
    path = os.path.join(os.path.dirname(__file__),'../tmp/{}'.format(input_path))
    if not input_path:
        path = os.path.join(os.path.dirname(__file__),'../tmp/graph_sample')

    files = glob.glob('{}/*.in'.format(path))
    print('input_files:',files)

    for i,path in enumerate(files):
        print('-'*25)
        print('sample{}\n'.format(i))
        graph_draw(path)

if __name__=='__main__':
    main()

# %%
