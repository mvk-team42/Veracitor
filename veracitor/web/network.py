
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
    neighbor_queue = [name]

    #for i in range(0, int(depth)):
    while neighbor_queue:
        new_queue = []
        for node in neighbor_queue:
            if not node in neighbors:
                neighbors.append(node)
                new_queue = new_queue + gn.successors(node) + gn.predecessors(node)
        neighbor_queue = new_queue

    #neighbors = list(set(itertools.chain.from_iterable(neighbors)))

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

#    res = search.get_producers.delay(name, type_of)
#    store_job_result(res)
#    return jsonify(job_id=res.id)

# def callback_function(trust):
#     pass
#     # TODO
#     # callback.set_item(trust)

# """
# Starts a SUNNY procedure given a source and sink producer.

# """
# @app.route('/calculate_sunny_value', methods=['GET','POST'])
# def calculate_sunny_value():

#     if request.method == 'POST':
#         procedure = {}
#         error = {
#             'message' : 'none',
#             'type' : 'none'
#         }

#         if request.form:
#             f = request.form

#             if not f['source']:
#                 error = {
#                     'message': 'No source node specified.',
#                     'type': 'no_source'
#                 }
#             if not f['sink']:
#                 error = {
#                     'message': 'No sink node specified.',
#                     'type': 'no_sink'
#                 }
#             if not f['tag']:
#                 error = {
#                     'message': 'No tag specified',
#                     'type': 'no_tag'
#                 }

#             if error['type'] == 'none':
#                 id = callback.get_unique_id()

#                 trust = compute_trust(gn.get_global_network(),
#                                       f['source'], f['sink'],
#                                       tag=f['tag'], callback=callback_function)

#                 procedure = {
#                     'message': 'Started SUNNY procedure',
#                     'callback_url': '/check_sunny_procedure',
#                     'trust': trust,
#                     'id': id
#                 }
#         else:
#             error = {
#                 'message': 'Form data error.',
#                 'type': 'form_error'
#             }

#         return json.dumps({ 'error': error, 'procedure': procedure })

#     return redirect(url_for('index'))

# """
# Handles the connection between the client and its currently
# running SUNNY procedures.

# """
# @app.route('/check_sunny_procedure', methods=['GET','POST'])
# def check_sunny_procedure():

#     if request.method == 'POST':
#         procedure = {}
#         error = {
#             'message' : 'none',
#             'type' : 'none'
#         }

#         if request.form:
#             f = request.form

#             if not f['id']:
#                 error = {
#                     'message': 'No id specified.',
#                     'type': 'no_source'
#                 }

#             if error['type'] == 'none':
#                 item = callback.check_id(f['id'])

#                 if item:
#                     procedure = {
#                         'status': 'done',
#                         'trust': item
#                     }
#                 else:
#                     procedure = {
#                         'status': 'processing'
#                     }

#         else:
#             error = {
#                 'message': 'Form data error.',
#                 'type': 'form_error'
#             }

#         return json.dumps({ 'error': error, 'procedure': procedure })

#     return redirect(url_for('index'))
