import sys, pandas as pd
from drepr import Graph

fpath = sys.argv[1]

node_file = f"{fpath}.node"
edge_file = f"{fpath}.edge"

graph = Graph.from_drepr_output_file(node_file, edge_file)

for class_name in graph.class2nodes:
    if class_name is None:
        continue

    data = []
    for node in graph.iter_nodes_by_class(class_name):
        node.data.pop('@type')
        data.append(node.data)

    output = f"{fpath}.{class_name}.csv"
    pd.DataFrame(data).to_csv(output, index=True)