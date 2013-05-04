from veracitor.algorithms import tidaltrust as tt

def sunny(graph, source, sink, tag="weight"):
    epsilon = 0.2
    # List of nodes to exclude
    decision = []
    bayesianNetwork = generate_bn(graph,source,sink,tag)
    leaves = (n for n,d in graph.out_degree_iter() if d == 0)
    for leaf in leaves:
        bounds = sample_bounds(bayesianNetwork, source, sink, {}, 100)
        source_lower = bounds[source][0]
        source_upper = bounds[source][1]
        for leaf in leaves:
            bounds[leaf] = [1,1]
            bounds = sample_bounds(bayesianNetwork, source, sink, bounds, 100)
            if not abs(bounds[source][0] - source_lower) < epsilon and abs(bounds[source][1] - source_upper) < epsilon:
                decision.append(leaf)

    return tt.compute_trust(bayesianNetwork, source, sink, decision, tag)

    

