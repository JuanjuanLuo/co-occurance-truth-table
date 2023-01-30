
import random
import numpy as np
import itertools
import networkx as nx
import matplotlib.pyplot as plt


def cor_network(leng,num_writer,p):
    nocor=set([1,2,3,4,5])
    cor=set()
    while len(cor)<leng:
        if random.random()<=p:
            cor.add(num_writer)
        else:
            if (num_writer-1 not in cor )and (cor.isdisjoint(nocor)==False):
                cor.add(random.randint(6,num_writer))
            else:
                cor.add(random.randint(1,num_writer))
    return list(cor)


def createNetwork(n,num_writer,p=0.15):
    matrix = np.zeros((n, num_writer))
    corset=set()
    for i in range(n):
        leng=random.randint(2,5) #Number of co-authors
        cor=cor_network(leng,num_writer,p)
        for writer in cor:
            matrix[i,writer-1]=1
        tuple_cor=tuple(sorted(list(cor)))
        corset.add(tuple_cor)
        cor.clear()
    TruthTable=np.unique(matrix,axis=0)
    return TruthTable,corset


def sensitivity(TruthTable,num_writer):
    #Returns the most sensitive node, TruthTable: truth table, num_writer: number of nodes
    positiveSensitivity=dict()

    for writer in range(num_writer):
        positiveSensitivity[writer+1] = 0
        for co in range(len(TruthTable)):
            if TruthTable[co][writer]==1:
                temp=np.copy(TruthTable)
                temp[co][writer]=0
                #If a node in the co-occurrence pattern is sensitive, 
                # the new co-occurrence pattern after the node is flipped should be the one that did not exist before,
                #  otherwise the repeated co-occurrence pattern will occur
                if len(temp)==len(np.unique(temp,axis=0)):
                    positiveSensitivity[writer+1] += 1
    # print(positiveSensitivity)
    maxPS=max(positiveSensitivity,key=lambda k:positiveSensitivity[k])
    return maxPS


def centrality(num_writer,corset):
    #Returns the node with the greatest centrality 
    # num_writer: the number of nodes, corset: the set of coauthors
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
    # print(degree,between,flowbetween)
    maxDC=max(dict_degree,key=lambda k:dict_degree[k])
    maxBC=max(between,key=lambda k:between[k])
    maxFBC=max(flowbetween,key=lambda k:flowbetween[k])
    return maxDC,maxBC,maxFBC
        
#Repeat 1000 times
n=1000
# Twelve samples were sampled 1500 times and the network was formed after removing duplicates
K=1500 
num=12
node_PS=[0]*num
node_DC=[0]*num
node_BC=[0]*num
node_FBC=[0]*num

for i in range(n):
    TruthTable,corset=createNetwork(K,num)
    # print(len(TruthTable),len(corset))

    maxPS=sensitivity(TruthTable,num)
    node_PS[maxPS-1] += 1
    maxDC,maxBC,maxFBC=centrality(num,corset)

    node_DC[maxDC-1] += 1
    node_BC[maxBC-1] += 1
    node_FBC[maxFBC-1] += 1
print(node_PS,node_DC,node_BC,node_FBC,sep='\n')



