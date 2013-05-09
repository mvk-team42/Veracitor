
import itertools

from flask import Flask, render_template, request, redirect, url_for, jsonify, session, abort

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
        log(request.form)
        source = request.form['source']
        target = request.form['target']
    except Exception as e:
        log("Exception: "+str(e)+"\nMsg: "+e.message+"\n");
        abort(400)

    # TODO fix the global network...
    gn = nm.build_network_from_db()

    try:
        nodes = nx.shortest_path(gn, source, target)
    except nx.exception.NetworkXNoPath:
        nodes = []

    data = {
        'source': extractor.entity_to_dict(extractor.get_producer(source)),
        'target': extractor.entity_to_dict(extractor.get_producer(target)),
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
        log(request.form)
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
                    neighbor_queue += gn.successors(node)
            layer = neighbor_queue
    else:
        layer = [name]
        for i in range(0, depth + 1):
            neighbor_queue = []
            for node in layer:
                if node not in neighbors:
                    neighbors.append(node)
                    neighbor_queue += gn.successors(node)
                    # exponential growth :(
            layer = neighbor_queue

    data = {}

    for node in neighbors:
        prod = extractor.get_producer(node)

        data[node] = extractor.entity_to_dict(prod)

    return jsonify(neighbors=data)

@app.route('/jobs/network/rate/information', methods=['GET','POST'])
def network_rate_information():
    """Rates an information object under its tag from a given producer.

    URL Structure:
        /jobs/network/rate_information

    Method:
        POST

    Parameters:
        prod (str): The producer.
        url (str): The URL.
        rating (int): The rating.

    Returns:
        Nothing.

    Errors:
        400 - Bad syntax/No name/type in request
        404 - Not found
        405 - Method not allowed

    """
    if not request.method == 'POST':
        abort(405)
    try:
        prod = request.form['prod']
        url = request.form['url']
        rating = int(request.form['rating'])
    except:
        abort(400)

    try:
        p = extractor.get_producer(prod)
        i = extractor.get_information(url)
    except:
        abort(404)

    p.rate_information(i, rating)

    return jsonify(data={'prod': extractor.entity_to_dict(p),
                         'info': extractor.entity_to_dict(i),
                         'rating': rating})

@app.route('/jobs/network/rate/producer', methods=['GET','POST'])
def network_rate_producer():
    """Rates a producer object under a given tag from a given producer.

    URL Structure:
        /jobs/network/rate_information

    Method:
        POST

    Parameters:
        source (str): The source producer.
        target (str): The target producer.
        tag (str): The tag.
        rating (int): The rating.

    Returns:
        Nothing.

    Errors:
        400 - Bad syntax/No name/type in request
        404 - Not found
        405 - Method not allowed

    """
    if not request.method == 'POST':
        abort(405)
    try:
        log(request.form)
        source = request.form['source']
        target = request.form['target']
        tag = request.form['tag']
        rating = int(request.form['rating'])
    except:
        abort(400)

    try:
        ps = extractor.get_producer(source)
        pt = extractor.get_producer(target)
        t = extractor.get_tag(tag)
    except:
        abort(404)

    ps.rate_source(pt, t, rating)

    return jsonify({'source': extractor.entity_to_dict(ps),
                    'target': extractor.entity_to_dict(pt),
                    'tag': extractor.entity_to_dict(t),
                    'rating': rating})

@app.route('/jobs/network/add_to_group', methods=['GET','POST'])
def add_to_group():

    if not request.method == 'POST':
        abort(405)
    try:
        user = extractor.get_user(session['user_name'])
        producer = extractor.get_producer(request.form['producer'])
        user.add_to_group(request.form['group_name'], producer)
        return "Success"
    except Exception, e:
        log(e)
        abort(400)

    return ''
