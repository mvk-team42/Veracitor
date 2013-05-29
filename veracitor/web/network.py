
import itertools

from flask import Flask, render_template, request, redirect, url_for, jsonify, session, abort

import json
import networkx as nx

import time

from veracitor.web import app
from veracitor.web.utils import store_job_result
import veracitor.tasks.network as network

from ..database import extractor, networkModel as nm
from ..algorithms.tidaltrust import compute_trust

log = app.logger.debug

@app.route('/jobs/network/path', methods=['GET','POST'])
def get_shortest_path():
    """Returns a path from the given source node to the given target node.

    URL Structure:
        /jobs/network/path

    Method:
        POST

    Parameters:
        source (str): The name of the source producer.
        target (str): The name of the target producer.
        tag (str): The tag name; '' if not specified.

    Optional parameters:
        tag (str): If specified, only edges with this tag will be considered.

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
        try:
            tag = request.form['tag']
        except:
            tag = ''
    except Exception as e:
        abort(400)

    res = network.get_shortest_path.delay(source, target, tag)
    store_job_result(res)
    return jsonify(job_id=res.id)


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

    Optional parameters:
        tag (str): If specified, only edges with this tag will be considered.

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

        try:
            tag = request.form['tag']
        except:
            tag = None
    except:
        abort(400)

    # TODO fix the global network...
    gn = nm.build_network_from_db()

    log("Ding dong! Is there a tag???????")
    if tag:
        log("Yup! It's a tag! And it's: "+tag)
        gn = _filter_network_by_tag(gn, tag)

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
                    neighbor_queue += gn.successors(node) + gn.predecessors(node)
            layer = neighbor_queue
    else:
        layer = [name]
        for i in range(0, depth + 1):
            neighbor_queue = []
            for node in layer:
                if node not in neighbors:
                    neighbors.append(node)
                    neighbor_queue += gn.successors(node) + gn.predecessors(node)
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
        source_prod (str): The producer.
        info_prod (str): The information producer/publisher.
        url (str): The information URL.
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
        prod = request.form['source_prod']
        info_prod = request.form['info_prod']
        url = request.form['url']
        rating = int(request.form['rating'])
    except:
        abort(400)

    try:
        p = extractor.get_producer(prod)
        ip = extractor.get_producer(info_prod)
        i = extractor.get_information(url)
    except:
        abort(404)

    p.rate_information(i, rating)

    return jsonify({'source_prod': extractor.entity_to_dict(p),
                    'info_prod': extractor.entity_to_dict(ip),
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
        user = extractor.get_user(request.form['user_name'])
        producer = extractor.get_producer(request.form['producer'])
        user.add_to_group(request.form['group_name'], producer)
        return "Success"
    except Exception, e:
        log(e)
        abort(400)

    return ''

@app.route('/jobs/network/paths_from_producer_lists', methods=['GET','POST'])
def paths_from_producer_lists():
    """Returns a path of json objects from dicts of producer names,
       stored in a dict.

    URL Structure:
        /jobs/network/path_from_producer_list

    Method:
        POST

    Parameters:
        path (dict): A dict of lists of producer names.

    Returns:
        A path stored as a dict of producer dicts.

    Errors:
        400 - Bad syntax/No name/type in request
        404 - Not found
        405 - Method not allowed

    """
    if not request.method == 'POST':
        abort(405)

    try:
        log(request.form)
        paths = json.loads(request.form['paths'])
    except:
        abort(400)

    data = []

    try:
        for nodes in paths:
            data.append({
                'source': nodes[0],
                'target': nodes[-1],
                'nodes': {},
                'edges': {},
                'ghosts': {}
            })

            for i, node in enumerate(nodes):
                prod = extractor.get_producer(node)

                for n in prod.source_ratings.keys():
                    if n not in nodes:
                        data[-1]['ghosts'][n] = node

                data[-1]['nodes'][node] = extractor.entity_to_dict(prod)

                if i < len(nodes) - 1:
                    data[-1]['edges'][node] = nodes[i + 1]
    except:
        abort(404)

    return jsonify(paths=data)
