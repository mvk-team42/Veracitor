
import itertools

from flask import Flask, render_template, request, redirect, url_for, jsonify

from veracitor.web import app

from ..database import extractor, networkModel as nm
from ..algorithms.tidaltrust import compute_trust

log = app.logger.debug

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
        Upon success, returns an object with the job_id, ex:
        {"job_id": "baad-f00d-dead-beefs-15"}

    Result when finished:
        An object with the producer data found.

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
                    neighbor_queue += gn.successors(node) + gn.predecessors(node)
            layer = neighbor_queue
    else:
        layer = [name]
        for i in range(0, depth):
            neighbor_queue = []
            for node in layer:
                if node not in neighbors:
                    neighbors.append(node)
                    neighbor_queue += gn.successors(node) + gn.predecessors(node)
            layer = neighbor_queue

    log(neighbors)

    data = {}

    for node in neighbors:
        prod = extractor.get_producer(node)
        source_ratings = [{'name' : s.source.name,
                           'tag' : s.tag.name,
                           'rating': s.rating }
                          for s in prod.source_ratings]
        data[node] = {'name' : prod.name,
                      'description' : prod.description,
                      'url' : prod.url,
                      'type_of' : prod.type_of,
                      'source_ratings' : source_ratings}

    return jsonify(neighbors=data,debug=neighbors)
