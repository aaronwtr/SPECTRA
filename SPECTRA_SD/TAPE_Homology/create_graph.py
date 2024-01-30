import pickle
import json
similarity = pickle.load(open('protein_similarity', 'rb'))

def extract_data(filenames):
    id_to_data = {}
    for filename in filenames:
        f = open(filename)
        data = json.load(f)

        for entry in data:
            id_to_data[entry['id']] = {}
            id_to_data[entry['id']]['primary'] = entry['primary']
    return id_to_data


train_to_data = extract_data(['remote_homology/remote_homology_train.json'])
val_to_data = extract_data(['remote_homology/remote_homology_valid.json'])
family_to_data = extract_data(['remote_homology/remote_homology_test_family_holdout.json'])
fold_to_data = extract_data(['remote_homology/remote_homology_test_fold_holdout.json'])
superfamily_to_data = extract_data(['remote_homology/remote_homology_test_superfamily_holdout.json'])

train_sequences = [train_to_data[i]['primary'] for i in train_to_data]
val_sequences = [val_to_data[i]['primary'] for i in val_to_data]
family_sequences = [family_to_data[i]['primary'] for i in family_to_data]
fold_sequences = [fold_to_data[i]['primary'] for i in fold_to_data]
superfamily_sequences = [superfamily_to_data[i]['primary'] for i in superfamily_to_data]

import networkx as nx

def construct_graph(seq):
    G = nx.Graph()
    n = len(seq)
    print("Constructing graph")
    for i in range(n):
        for j in range(i+1, n):
            try:
                if similarity[(i, j)] > 0.3:
                   G.add_edge(i, j)
            except Exception:
                if similarity[(j, i)] > 0.3:
                   G.add_edge(i, j)

    return G

G = construct_graph(train_sequences+val_sequences)
nx.write_gexf(G, "homology_graph.gexf")
print(G.number_of_nodes())
print(G.number_of_edges())
print(nx.number_connected_components(G))
