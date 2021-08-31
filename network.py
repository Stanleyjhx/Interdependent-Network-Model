import networkx as nx
import random as rd
import numpy as np
import matplotlib.pyplot as plt
from pyvis.network import Network



G = nx.DiGraph()
N = 20 # Number of nodes, to be tuned
network = G


# set changing prob params
init_0 = 0.05 #initial broken part
spon_0 = 0.05  #edge breaking rate
spon_1 = 0.1  #edge repairing rate



# initialize the state of the starting network -- using binomial dist
for i in range(N):
    network.add_node(i,state =np.random.binomial(1,1-init_0))

# populate the network, add edges
for i in range(N):
    for j in range(0,i-1):
        flag1 = rd.uniform(0,10)
        flag2 = rd.uniform(0,10)
        if flag1 > 5:
            network.add_edge(i,j)
        if flag2 > 5:
            network.add_edge(j,i)


# main loop of the algorithm

count = 1
iter_list = []
vitality_list = []
while 1:
    for i in range(N):
        flag_0 = np.random.binomial(1,spon_0)
        flag_1 = np.random.binomial(1,spon_1)
        if flag_0 == 1:
            network.nodes[i]["state"] = 0
        if flag_1 == 1:
            network.nodes[i]["state"] = 1
    for i in range (N):
        pre = network.predecessors(i)
        pre_sum = 0
        for j in list(pre):
            pre_sum = pre_sum + network.nodes[j]["state"]
        if pre_sum < len(list(pre)):
            network.nodes[i]["state"] = 0

    state_sum = 0
    for node in range(N):
        state_sum = state_sum + nx.get_node_attributes(network,"state")[node]
    vitality = state_sum / N
    print("iteration:",count," vitality:",vitality)
    iter_list.append(count)
    vitality_list.append(vitality)
    count = count + 1
    if state_sum == 0:
        break


net = Network(notebook=True)
net.from_nx(network)
net.show("example.html")

#np.savetxt('data.csv', (iter_list, vitality_list), delimiter=',')

plt.plot(iter_list, vitality_list, color='green', linewidth=2, label="vitality")
plt.legend(loc="lower right")

# setting x and y axis range
plt.ylim(0, 1)
#plt.xlim(1, 2000)

# naming the x axis
plt.xlabel('Iterations')
# naming the y axis
plt.ylabel('Vitality')

# giving a title to my graph
plt.title('N=20,init_br=0.05,br=0.05,rr=0.1')

# function to show the plot
plt.show()