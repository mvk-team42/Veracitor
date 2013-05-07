
import itertools

from flask import Flask, render_template, request, redirect, url_for, jsonify

import networkx as nx

from veracitor.web import app

from ..database import extractor, networkModel as nm
from ..algorithms.tidaltrust import compute_trust

log = app.logger.debug

@app.route('/jobs/network/path', methods=['GET','POST'])
def get_shortest_path():
    """Returns a path from the given source node to the given target node.

    URL Structure:
        /jobs/network/neighbors

    Method:
        POST

    Parameters:
        source (str): The name of the source producer.
        target (str): The name of the target producer.

    Returns:
        An object with the found path.

    Errors:
        400 - Bad syntax
        405 - Method not allowed

    """
    if not request.method == 'POST':
        abort(405)
    try:
        source = request.form['source']
        target = request.form['target']
    except:
        abort(400)

    # TODO fix the global network...
    gn = nm.build_network_from_db()

    try:
        nodes = nx.shortest_path(gn, source, target)
    except nx.exception.NetworkXNoPath:
        nodes = []

    data = {
        'source': source,
        'target': target,
        'nodes': [],
        'ghosts': []
    }

    for node in nodes:
        prod = extractor.get_producer(node)

        for k, v in prod.source_ratings.items():
            if k not in nodes:
                data['ghosts'].append(k)

        data['nodes'].append(extractor.entity_to_dict(prod))

    return jsonify(path=data)

@app.route('/jobs/network/neighbors', methods=['GET','POST'])
def get_neighbors():
    """Returns the neighbors to the given source producer at
    the given depth.

    URL Structure:
        /jobs/network/neighbors

    Method:
        POST

    Parameters:
        name (str): The name of the source producer.
        depth (int): The neighbour depth.

    Returns:
        An object with the found neighbours.

    Errors:
        400 - Bad syntax/No name/type in request
        405 - Method not allowed

    """
    if not request.method == 'POST':
        abort(405)
    try:
        name = request.form['name']
        depth = request.form['depth']
    except:
        abort(400)

    # TODO fix the global network...
    gn = nm.build_network_from_db()

    neighbors = []

    #for i in range(0, int(depth)):
    depth = int(depth)

    if depth < 0:
        layer = [name]
        while layer:
            neighbor_queue = []
            for node in layer:
                if node not in neighbors:
                    neighbors.append(node)
                    neighbor_queue += gn.successors(node)# + gn.predecessors(node)
            layer = neighbor_queue
    else:
        layer = [name]
        for i in range(0, depth + 1):
            neighbor_queue = []
            for node in layer:
                if node not in neighbors:
                    neighbors.append(node)
                    neighbor_queue += gn.successors(node)# + gn.predecessors(node)
            layer = neighbor_queue

    data = {}

    for node in neighbors:
        prod = extractor.get_producer(node)

        data[node] = extractor.entity_to_dict(prod)

    return jsonify(neighbors=data)
