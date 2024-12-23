from collections import defaultdict
from itertools import combinations


# Step 1: Parse the input file
def parse_input(file_path):
    graph = defaultdict(set)
    with open(file_path, "r") as file:
        for line in file:
            a, b = line.strip().split("-")
            graph[a].add(b)
            graph[b].add(a)
    return graph


# Step 2: Find the largest clique using Bron-Kerbosch algorithm
def bron_kerbosch(R, P, X, graph, cliques):
    if not P and not X:
        cliques.append(R)
        return

    for v in list(P):
        bron_kerbosch(R | {v}, P & graph[v], X & graph[v], graph, cliques)
        P.remove(v)
        X.add(v)


def find_largest_clique(graph):
    cliques = []
    nodes = set(graph.keys())
    bron_kerbosch(set(), nodes, set(), graph, cliques)

    # Find the largest clique
    largest_clique = max(cliques, key=len)
    return sorted(largest_clique)


if __name__ == "__main__":
    file_path = "input/day23.txt"
    graph = parse_input(file_path)

    largest_clique = find_largest_clique(graph)
    password = ",".join(largest_clique)
    print("Password to get into the LAN party:", password)
