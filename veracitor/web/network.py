from flask import Flask, render_template, request, redirect, url_for

from veracitor.web import app
from veracitor.web.crawler import crawl_callback, get_unique_crawl_id

from ..database import globalNetwork as gn
from ..algorithms.tidaltrust import compute_trust

import json

"""
Starts a SUNNY procedure given a source and sink producer.

"""
@app.route('/calculate_sunny_value', methods=['GET','POST'])
def calculate_sunny_value():

    if request.method == 'POST':
        procedure = {}
        error = {
            'message' : 'none',
            'type' : 'none'
        }

        if request.form:
            f = request.form

            if not f['source']:
                error = {
                    'message': 'No source node specified.',
                    'type': 'no_source'
                }
            if not f['sink']:
                error = {
                    'message': 'No sink node specified.',
                    'type': 'no_sink'
                }

            if error['type'] == 'none':
                id = get_unique_crawl_id()

                #compute_trust(gn.get_global_network(),

                procedure = {
                    'message': 'Started SUNNY procedure',
                    'callback_url': '/check_sunny_procedure',
                    'id': id
                }
        else:
            error = {
                'message': 'Form data error.',
                'type': 'form_error'
            }

        return json.dumps({ 'error': error, 'procedure': procedure })

    return redirect(url_for('index'))

"""
Handles the connection between the client and its currently
running SUNNY procedures.

"""
@app.route('/check_sunny_procedure', methods=['GET','POST'])
def check_sunny_procedure():

    if request.method == 'POST':
        procedure = {}
        error = {
            'message' : 'none',
            'type' : 'none'
        }

        if request.form:
            f = request.form

            if not f['id']:
                error = {
                    'message': 'No id specified.',
                    'type': 'no_source'
                }

            if error['type'] == 'none':
                # check SUNNY procedure

                procedure = {
                    'status': 'done',
                    'trust': 3
                }

        else:
            error = {
                'message': 'Form data error.',
                'type': 'form_error'
            }

        return json.dumps({ 'error': error, 'procedure': procedure })

    return redirect(url_for('index'))
