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


#Taks 3

def dfs(graph, start):
    """
    Input: an adjacency list (undirected or directed), a start vertex.
    Output: list[str], the vertices reachable from start, in the order you first 
    visit them.
    Ties: when a vertex has several unvisited neighbours, visit them in sorted 
    order — this is exactly what makes your hand-trace on the handout and your 
    code agree, not just on the set of vertices but on the order too.
    """
    
    visited = set()
    result = []

    def dfs_helper(v):
        visited.add(v)
        result.append(v)
        for neighbor in sorted(graph[v]):
            if neighbor not in visited:
                dfs_helper(neighbor)

    dfs_helper(start)
    print(result)
    return result

def connected_components(graph):
    """
    Input: an adjacency list.
    Output: list[set[str]], one set per maximal connected component.
    Hint: repeatedly call dfs from any vertex that is not yet in any component 
    you have found.
    Self-check: the components must partition the vertex set of the graph — their 
    union is exactly set(graph), and no two components share a vertex. Check this 
    with set operations on your own output.
    """

    components = []
    visited = set()

    for vertex in graph:
        if vertex not in visited:
            component = set(dfs(graph, vertex))
            components.append(component)
            visited.update(component)

    print(components)
    return components

def is_weakly_connected(graph):
    """
    Input: a directed adjacency list.
    Output: bool, true exactly when treating every directed edge as undirected 
    (its "shadow") gives a single connected component.
    Hint: build the undirected shadow of the graph — for every edge u → v, add v to 
    u's and u to v's neighbour list in a fresh adjacency list — then reuse 
    connected_components on the shadow.
    """

    # Build the undirected shadow of the directed graph
    shadow_graph = {}
    for u in graph:
        if u not in shadow_graph:
            shadow_graph[u] = []
        for v in graph[u]:
            if v not in shadow_graph:
                shadow_graph[v] = []
            shadow_graph[u].append(v)
            shadow_graph[v].append(u)

    # Check if the shadow graph has a single connected component
    components = connected_components(shadow_graph)
    is_connected = len(components) == 1
    print(is_connected)
    return is_connected

    #Task 4

def eulerian_type(graph, directed=False):
    """
    Input: an adjacency list; directed.
    Output: one of the literal strings "circuit", "path", "none".
    Hint: reuse degrees/in_out_degree and connected_components/is_weakly_connected 
    from Tasks 1 and 3. The undirected and directed rules are genuinely different — 
    write them as two clearly separate branches, do not try to force them into one 
    shared formula.
    Run it on the graphs from the handout: your function's verdict must agree with 
    what you derived by hand, for all of G1, G3, G4, G5a, G5b and Königsberg. 
    If any of them disagree, do not assume the code is the one that is wrong — 
    recheck your hand reasoning too; either could be the bug.
    Self-checks (these must hold for any implementation, not just a correct one — 
    if one of them fails, you have found a bug, in your code or in your by-hand 
    reasoning):
    Delete any single edge from a graph your function currently calls "circuit"; 
    it must now return "path" or "none", never "circuit" again. Removing one edge 
    can only break the even-degree condition at its two endpoints — it can never 
    fix a connectivity problem that was not already there. Try this on every graph 
    from the handout that your function calls "circuit".
    Before calling your function, count the odd-degree vertices (undirected) or the 
    excess (out − in) of every vertex (directed) yourself. If an undirected graph 
    has anything other than 0 or 2 odd-degree vertices, your function must return 
    "none". If a directed graph has any vertex with an excess of +2, −2, or 
    anything besides 0/+1/−1, it must also return "none" — a single vertex with 
    excess 2 makes an Eulerian path just as impossible as four odd-degree vertices 
    do in the undirected case, even though its in+out degree sum can still be even.
    A disconnected (or, for directed graphs, not weakly connected) graph must 
    always come back "none", no matter what the degrees say. Test this directly 
    on G1.
    For a directed graph, reverse every single edge. If the original graph was 
    "circuit", the reversed graph must still be "circuit" (in-degree and out-degree 
    simply swap roles at every vertex; weak connectivity is unaffected by reversal). 
    Try this on every directed graph from the handout that your function calls 
    "circuit".
    """

    if directed:
        in_degree, out_degree = in_out_degree(graph)
        excess = {v: out_degree[v] - in_degree[v] for v in graph}
        
        # Check weak connectivity
        if not is_weakly_connected(graph):
            return "none"
        
        # Count vertices with excess +1 and -1
        plus_one = sum(1 for e in excess.values() if e == 1)
        minus_one = sum(1 for e in excess.values() if e == -1)
        
        if plus_one == 0 and minus_one == 0:
            return "circuit"
        elif plus_one == 1 and minus_one == 1:
            return "path"
        else:
            return "none"
    else:
        degree_dict = degrees(graph)
        
        # Check connectivity
        components = connected_components(graph)
        if len(components) > 1:
            return "none"
        
        # Count odd-degree vertices
        odd_count = sum(1 for d in degree_dict.values() if d % 2 != 0)
        
        if odd_count == 0:
            return "circuit"
        elif odd_count == 2:
            return "path"
        else:
            return "none"

eulerian_type(graph, directed=True)

