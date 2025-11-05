from collections import defaultdict


# Step 1: Parse the input file
def parse_input(file_path):
    graph = defaultdict(set)
    with open(file_path, "r") as file:
        for line in file:
            a, b = line.strip().split("-")
            graph[a].add(b)
            graph[b].add(a)
    return graph


# Step 2: Find all triangles in the graph
def find_triangles(graph):
    triangles = []
    for node in graph:
        neighbors = graph[node]
        for neighbor in neighbors:
            common_neighbors = neighbors & graph[neighbor]
            for common in common_neighbors:
                triangle = tuple(sorted([node, neighbor, common]))
                if triangle not in triangles:
                    triangles.append(triangle)
    return triangles


# Step 3: Filter triangles containing a node starting with 't'
def filter_triangles(triangles):
    return [
        triangle
        for triangle in triangles
        if any(node.startswith("t") for node in triangle)
    ]


# Step 4: Main execution
if __name__ == "__main__":
    file_path = "input/day23.txt"
    graph = parse_input(file_path)
    all_triangles = find_triangles(graph)
    filtered_triangles = filter_triangles(all_triangles)
    print("Total triangles with a node starting with 't':", len(filtered_triangles))
