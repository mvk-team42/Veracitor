# network.py
# ===========
# Defines tasks for networking. :)

try:
    from veracitor.tasks.tasks import taskmgr
except:
    from tasks import taskmgr

from veracitor.tasks.tasks import db, gn

from celery.utils.log import get_task_logger

import datetime
import networkx as nx

logger = get_task_logger(__name__)

@taskmgr.task
def get_shortest_path( source, target, tag ):

    data = {
        'source': db.extractor.entity_to_dict(db.extractor.get_producer(source)),
        'target': db.extractor.entity_to_dict(db.extractor.get_producer(target)),
        'nodes': {},
        'edges': {},
        'ghosts': {},
        'tag': tag
    }

    try:
        if tag:
            dgn = _filter_network_by_tag(gn, tag)
            nodes = nx.shortest_path(dgn, source, target)
        else:
            nodes = nx.shortest_path(gn, source, target)
    except:
        nodes = []

    for i, node in enumerate(nodes):
        prod = db.extractor.get_producer(node)

        neighbors = gn.successors(node) + gn.predecessors(node)
        for n in neighbors:
            if n not in nodes:
                data['ghosts'][n] = node

        data['nodes'][node] = db.extractor.entity_to_dict(prod)

        if i < len(nodes) - 1:
            data['edges'][node] = nodes[i + 1]

    return { 'path': data }


@taskmgr.task
def get_neighbors( name, tag, depth ):
    if tag:
        ngn = _filter_network_by_tag(gn, tag)
    else:
        ngn = gn

    neighbors = []

    depth = int(depth)

    # Fetch neighbors
    if depth < 0:
        layer = [name]
        while layer:
            neighbor_queue = []
            for node in layer:
                if node not in neighbors:
                    neighbors.append(node)
                    neighbor_queue += ngn.successors(node) + ngn.predecessors(node)
            layer = neighbor_queue
    else:
        layer = [name]
        for i in range(0, depth + 1):
            neighbor_queue = []
            for node in layer:
                if node not in neighbors:
                    neighbors.append(node)
                    neighbor_queue += ngn.successors(node) + ngn.predecessors(node)
                    # exponential growth :(
            layer = neighbor_queue

    data = {}

    for node in neighbors:
        prod = db.extractor.get_producer(node)

        data[node] = db.extractor.entity_to_dict(prod)

    return { 'neighbors': data }


def _filter_network_by_tag(network, tag):
    """
    Creates a graph from input network containing only the edges in network
    that have a weight/rating under the specified tag.

    """
    Gtagged = nx.DiGraph()

    for n in network.nodes():
        for nn in network[n]:
            try:
                Gtagged.add_edge(n, nn, {tag:network[n][nn][tag]})
            except:
                pass

    return Gtagged
