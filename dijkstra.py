from cmath import inf
from turtle import color, width
from soupsieve import closest
from sqlalchemy import null
import networkx as nx
import matplotlib.pyplot as plt

# you may need to install networkx
#### here we are just reading and converting the graph into adjacency matrix

n = -1
graph = {}
G = nx.Graph()

file = open('graph.txt', 'r')
lines = file.readlines()

for line in lines:
    # first line is just number of edges in a graph
    if n == -1:
        n = line
        continue
    vals = line.split(" ")
    first = vals[0]
    second = vals[1]
    weight = vals[2]

    if first not in graph:
        graph[first] = {}
    if second not in graph:
        graph[second] = {}
    G.add_edge(first, second, color='g', weight=int(weight))
    graph[first][second] = int(weight)
    graph[second][first] = int(weight)



################################
### START OF DIJKSTRA ALGORITHM
###############################
def dijkstra(graph, start, goal):
    distances = {} # stores the min cost of reaching the node
    unvisitedNodes = graph # stores not visited nodes
    parents = {} # it will store the parent of nodes, 1 : 2 means that the 2 is the parent node of 1

    # set distances to nodes as infinity
    for i in graph:
        distances[i] = float('inf')
    
    # the cost of traveling from start to itself is zero
    distances[start] = 0

    # repeat until we don't visit all the nodes
    while unvisitedNodes:
        # take the unvisited node with lowest distance
        closestNode = None
        for node in unvisitedNodes:
            if closestNode is None or distances[node] < distances[closestNode]:
                closestNode = node

        # get the neighbors of the closestNode
        neighbors = graph[closestNode].items()

        # for each neighbor check if we can reach it with lower cost
        # if so update the distance
        for n, w in neighbors:
            if distances[closestNode] + w < distances[n]:
                distances[n] = distances[closestNode] +w
                parents[n] = closestNode

        # remove visited node
        unvisitedNodes.pop(closestNode)

    res = distances[goal]

    if res == inf:
        print("there is no path from {} to {}".format(start, goal))
    else:
        print('from {} to {} costs {}'.format(start, goal, res))

    # we will use the parents dictionary to build the path from start to goal
    path = [goal]
    while (goal in parents):
        path.append(parents[goal])
        goal = parents[goal]

    # path contains the list of nodes from start to end

    return {'path': path, 'cost': res}
##############################
### END OF DIJKSTRA ALGORITHM
#############################

# ask for inputs
start = input("please insert a starting vertex: ")
goal = input("please insert a goal vertex: ")
weights = graph.copy()

if (start not in graph or goal not in graph):
    print("the node {} or {} doesn't exists in graph".format(start, goal))
else:
    res = dijkstra(graph, start, goal)

    path = res['path']
    for i in range(len(path)-1):
        G.add_edge(path[i], path[i+1], weight=weights[path[i]][path[i+1]], color='r')
    
    colors = nx.get_edge_attributes(G,'color').values()
    weights = nx.get_edge_attributes(G,'weight').values()

    pos = nx.circular_layout(G)
    nx.draw(G, pos, 
            edge_color=colors, 
            width=[1],
            with_labels=True,
            node_color='lightgreen')
            
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.text(-1.1, 1.1, 'cost is {}'.format(res['cost']), fontsize = 16)
    plt.text(-1.047, -1.13, 'nodes on a path are {}'.format(path), fontsize = 10)
    plt.show()