E = (("P1", "P2"), ("P1", "P3"), ("P2", "P3"), ("P3", "P4"), ("P4", "P5"))

def build_adjacency_list(edges, directed=False):
    """
    Input: edges, a list of 2-tuples of vertex names; directed, a bool.

    Output: dict[str, list[str]]. If directed=False, every edge (u, v) 
    must appear on both sides: v in graph[u] and u in graph[v]. 
    If directed=True, (u, v) appears only as v in graph[u]. Every vertex 
    that occurs anywhere in edges must be a key of graph, even if its 
    neighbour list ends up empty.
    Hint: this is the adjacency-list representation from the slides, a dict 
    of lists, not a matrix. Two edges between the same pair of vertices 
    (a multigraph) are simply two entries in the list.
    """
    graph = {}
    for u, v in edges:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    print(graph)
    return graph


def degrees(graph):
    """
    Input: graph, an undirected adjacency list.
    Output: dict[str, int]: the degree of every vertex of graph, including vertices with 
    an empty neighbour list (degree 0).
    Hint: every undirected edge is already stored in both neighbour lists, so the degree 
    of v can be read from graph[v] alone.
    """
    
    degree = {}
    for vertex in graph:
        degree[vertex] = len(graph[vertex])
    print(degree)
    return degree

def in_out_degree(graph):
    """
    Input: graph, a directed adjacency list.
    Output: (in_degree, out_degree), two dict[str, int], keyed by every vertex.
    Hint: out_degree[v] is the length of graph[v]; in_degree needs one pass over every 
    neighbour list in graph, counting how often each vertex is mentioned.
    Self-check: sum(in_degree.values()) == sum(out_degree.values()) == len(edges) — every directed edge 
    contributes exactly one unit of out-degree and one unit of in-degree, somewhere.
    """

    in_degree = {}
    out_degree = {}
    
    # Initialize in_degree and out_degree for all vertices
    for vertex in graph:
        in_degree[vertex] = 0
        out_degree[vertex] = len(graph[vertex])
    
    # Count in-degrees by iterating through the adjacency list
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            if neighbor not in in_degree:
                in_degree[neighbor] = 0
            in_degree[neighbor] += 1
    
    print(in_degree, out_degree)       
    return in_degree, out_degree


graph = build_adjacency_list(E, directed=True)
in_degree, out_degree = in_out_degree(graph)
print(sum(in_degree.values()) == sum(out_degree.values()) == len(E))