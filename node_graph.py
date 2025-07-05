# Visualize node graph

import matplotlib.pyplot as plt
import json, sys
import networkx as nx
from node_lib import graph

print '\nNode image tools (Visualize node graph) v01a\n'

try:
    file_node=sys.argv[1]
except:
    print '->Error. No script'
    sys.exit (0)

with open(file_node) as jdf:
    data_io = json.load(jdf)

# Bringing format node to object type and sort by ID
sorted_names=sorted(data_io, key=lambda x : data_io[x]['id'])

GNode = graph
Node_graph=nx.DiGraph()

# Creating a graph
for _name in sorted_names:
    node = GNode(data_io[_name])

    if (node.type=='read'):
        Node_graph.add_node(node.name)

    if (node.type=='cc'):
        Node_graph.add_node(node.name)
        Node_graph.add_edge(node.link,node.name)

    if (node.type=='size'):
        Node_graph.add_node(node.name)
        Node_graph.add_edge(node.link,node.name)

    if (node.type=='rotate'):
        Node_graph.add_node(node.name)
        Node_graph.add_edge(node.link,node.name)

    if (node.type=='gradient'):
        Node_graph.add_node(node.name)

    if (node.type=='composite'):
        Node_graph.add_node(node.name)
        Node_graph.add_edge(node.link_a,node.name)
        Node_graph.add_edge(node.link_b,node.name)
        if (node.job=='mask'):
            Node_graph.add_edge(node.mask,node.name)

    if (node.type=='blur'):
        Node_graph.add_node(node.name)
        Node_graph.add_edge(node.link,node.name)

    if (node.type=='sharpen'):
        Node_graph.add_node(node.name)
        Node_graph.add_edge(node.link,node.name)

    if (node.type=='view'):
        Node_graph.add_node(node.name)
        Node_graph.add_edge(node.link,node.name)

    if (node.type=='write'):
        Node_graph.add_node(node.name)
        Node_graph.add_edge(node.link,node.name)

    if (node.type=='invert'):
        Node_graph.add_node(node.name)
        Node_graph.add_edge(node.link,node.name)        

pos=nx.spring_layout(Node_graph,iterations=30,weight=50,scale=1)
# Draw graph
for _graph in sorted_names:
    graph_ = GNode(data_io[_graph])
    if (graph_.type=='write' or graph_.type=='read'):
        nx.draw_networkx_nodes(Node_graph,pos,node_size=2000,alpha=0.5,
                               node_shape='s',node_color='r',nodelist=[graph_.name])
    if (graph_.type=='blur' or graph_.type=='sharpen'):
        nx.draw_networkx_nodes(Node_graph,pos,node_size=2000,alpha=0.5,
                               node_color='g',nodelist=[graph_.name])
    if (graph_.type=='gradient'):
        nx.draw_networkx_nodes(Node_graph,pos,node_size=2000,alpha=0.25,
                               node_shape='s',node_color='r',nodelist=[graph_.name])
    if (graph_.type=='composite'):
        nx.draw_networkx_nodes(Node_graph,pos,node_size=5000,alpha=0.5,
                               node_color='y',nodelist=[graph_.name])
    if (graph_.type=='cc' or graph_.type=='invert'):
        nx.draw_networkx_nodes(Node_graph,pos,node_size=2000,alpha=0.5,
                               node_color='b',nodelist=[graph_.name])
    if (graph_.type=='rotate' or graph_.type=='size'):
        nx.draw_networkx_nodes(Node_graph,pos,node_size=2000,alpha=0.3,
                               node_color='w',nodelist=[graph_.name])
    if (graph_.type=='view'):
        nx.draw_networkx_nodes(Node_graph,pos,node_size=2000,alpha=0.25,
                               node_shape='^',node_color='r',nodelist=[graph_.name])

nx.draw_networkx_labels(Node_graph,pos,
                        font_size=10,font_family='sans-serif')
nx.draw_networkx_edges(Node_graph,
                       pos,width=2,
                       alpha=0.5,
                       edge_color='g',
                       style='solid',
                       arrows=True,
                       )

#plt.savefig("node_graph3.png")
plt.show()
print '\nVisualize graph:',file_node,'completed'
