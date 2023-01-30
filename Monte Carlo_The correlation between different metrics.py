
import random
import numpy as np
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import scipy.stats as ss


def cor_network2(leng,num_writer):
    cor=set()
    while len(cor)<leng:
        cor.add(random.randint(1,num_writer))
    return list(cor)


def createNetwork(n,num_writer):
    matrix = np.zeros((n, num_writer))
    corset=set()
    for i in range(n):
        leng=random.randint(2,6)
        cor=cor_network2(leng,num_writer)
        for writer in cor:
            matrix[i,writer-1]=1
        tuple_cor=tuple(sorted(cor))
        corset.add(tuple_cor)
        cor.clear()
    TruthTable=np.unique(matrix,axis=0)

    return TruthTable,corset


def sensitivity(TruthTable,num_writer):
    positiveSensitivity=dict()

    for writer in range(num_writer):
        positiveSensitivity[writer+1] = 0
        for co in range(len(TruthTable)):
            if TruthTable[co][writer]==1:
                temp=np.copy(TruthTable)
                temp[co][writer]=0
                if len(temp)==len(np.unique(temp,axis=0)):
                    positiveSensitivity[writer+1] += 1
    # print(positiveSensitivity)
    PS=list()
    for i in sorted(positiveSensitivity):
        PS.append(positiveSensitivity[i])

    return PS

def centrality(num_writer,corset):
    adj = np.zeros((num_writer, num_writer))
    for cor in corset:
        for edge in itertools.combinations(cor,2):
            adj[edge[0]-1][edge[1]-1] += 1
            adj[edge[1]-1][edge[0]-1] += 1
    G=nx.Graph()
    for r in range(num_writer):
        for c in range(num_writer):
            if adj[r][c]>0:
                G.add_edge(r+1,c+1,weight=adj[r][c])
    pos=nx.spring_layout(G) # positions for all nodes

    degree=nx.degree(G,weight='weight')
    between=nx.betweenness_centrality(G,weight='weight',endpoints=False)
    flowbetween=nx.current_flow_betweenness_centrality(G,weight='weight')
    dict_degree=dict(degree)

    DC=list()
    BC=list()
    FBC=list()

    for i in range(1,num_writer+1):
        DC.append(dict_degree[i])
        BC.append(between[i])
        FBC.append(flowbetween[i])

    return DC,BC,FBC
        

n=100
K=10000
num=200
PS_DC=[]
PS_BC=[]
PS_FBC=[]
for i in range(n):
    TruthTable,corset=createNetwork(K,num)
    PS=sensitivity(TruthTable,num)
    DC,BC,FBC=centrality(num,corset)
    cor1,p1=ss.pearsonr(PS,DC)
    cor2,p2=ss.pearsonr(PS,BC)
    cor3,p3=ss.pearsonr(PS,FBC)
    PS_DC.append((cor1,p1))
    PS_BC.append((cor2,p2))
    PS_FBC.append((cor3,p3))
    
print(PS_DC,PS_BC,PS_FBC,sep='\n')


